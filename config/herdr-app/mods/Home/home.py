#!/usr/bin/env python3
"""Data for the project Home tab. Prints JSON; reads only.

  home.py sessions <folder> [--exact]   recent Claude Code sessions started in folder
                                        (or below it, unless --exact), newest first
  home.py repos <folder>                git repos at folder and one level below: branch,
                                        changed files, ahead/behind
  home.py prs <folder>                  open pull requests of those repos (gh)
"""
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, ".claude", "projects")
SKIP = {"node_modules", ".git", ".next", "dist", "build", ".venv", "vendor", "wp-content", "wp-includes", "wp-admin"}


def key(path):
    """Claude Code's project folder name for a cwd: every non-alphanumeric becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def folders(root, depth=4):
    """Real folders under root (Claude worktrees included), keyed the way Claude keys them."""
    out = {key(root): root}
    stack = [(root, 0)]
    while stack:
        d, n = stack.pop()
        if n >= depth:
            continue
        try:
            entries = os.scandir(d)
        except OSError:
            continue
        with entries:
            for e in entries:
                if e.is_dir(follow_symlinks=False) and e.name not in SKIP:
                    out.setdefault(key(e.path), e.path)
                    stack.append((e.path, n + 1))
    return out


def title_of(path):
    """The last AI or custom title in a session file (titles repeat, so read the tail)."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        for span in (262144, size):
            f.seek(max(0, size - span))
            found = None
            for line in f.read().splitlines():
                if b'"ai-title"' in line or b'"custom-title"' in line:
                    try:
                        d = json.loads(line)
                    except ValueError:
                        continue
                    found = d.get("customTitle") or d.get("aiTitle") or found
            if found or span >= size:
                return found


def sessions(root, exact):
    root = os.path.realpath(os.path.expanduser(root))
    want = key(root)
    places = {want: root} if exact else folders(root)
    rows = []
    for name in os.listdir(PROJECTS):
        if not (name == want if exact else (name == want or name.startswith(want + "-"))):
            continue
        cwd = places.get(name)
        if not cwd:
            continue  # a folder that's gone (an old worktree): can't resume there
        d = os.path.join(PROJECTS, name)
        for f in os.listdir(d):
            if f.endswith(".jsonl"):
                p = os.path.join(d, f)
                rows.append((os.path.getmtime(p), f[:-6], cwd, p))
    rows.sort(reverse=True)
    out = []
    for mtime, sid, cwd, p in rows[:40]:
        t = title_of(p)
        if not t:
            continue  # no title yet: usually an empty or one-line session
        rel = os.path.relpath(cwd, root)
        out.append({"id": sid, "title": t, "at": int(mtime), "cwd": cwd, "where": "" if rel == "." else rel.split(os.sep)[0]})
        if len(out) == 8:
            break
    return out


def git(args, cwd, timeout=8):
    r = subprocess.run(["git", "--no-optional-locks", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.stdout if r.returncode == 0 else None


def repo_dirs(root):
    root = os.path.realpath(os.path.expanduser(root))
    found = [root] if os.path.exists(os.path.join(root, ".git")) else []
    if not found or root != HOME:
        try:
            for e in sorted(os.scandir(root), key=lambda e: e.name.lower()):
                if e.is_dir() and not e.name.startswith(".") and os.path.exists(os.path.join(e.path, ".git")):
                    found.append(e.path)
        except OSError:
            pass
    return found


def repo(path):
    status = git(["status", "--porcelain=v2", "--branch", "--untracked-files=all"], path) or ""
    branch, ahead, behind, changed = None, 0, 0, 0
    for line in status.splitlines():
        if line.startswith("# branch.head "):
            branch = line.split(" ", 2)[2]
        elif line.startswith("# branch.ab "):
            a, b = line.split()[2:4]
            ahead, behind = int(a), -int(b)
        elif line and not line.startswith("#"):
            # Claude Code's own per-machine files are never committed: not "changes".
            if line.startswith("? ") and line[2:].startswith((".claude/settings.local.json", ".claude/worktrees/")):
                continue
            changed += 1
    return {"name": os.path.basename(path), "path": path, "branch": branch, "changed": changed, "ahead": ahead, "behind": behind}


def repos(root):
    with ThreadPoolExecutor(6) as pool:
        return list(pool.map(repo, repo_dirs(root)))


def prs_of(path):
    remote = git(["remote", "get-url", "origin"], path) or ""
    if "github.com" not in remote:
        return []
    try:
        r = subprocess.run(["gh", "pr", "list", "--state", "open", "--limit", "10", "--json",
                            "number,title,url,isDraft,reviewDecision,statusCheckRollup,author"],
                           cwd=path, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if r.returncode != 0:
        return []
    out = []
    for p in json.loads(r.stdout or "[]"):
        checks = [c.get("conclusion") or c.get("state") or c.get("status") for c in p.get("statusCheckRollup") or []]
        bad = any(c in ("FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED") for c in checks)
        pending = any(c in ("PENDING", "IN_PROGRESS", "QUEUED", "EXPECTED", None) for c in checks)
        out.append({"repo": os.path.basename(path), "number": p["number"], "title": p["title"], "url": p["url"],
                    "draft": p.get("isDraft", False), "review": p.get("reviewDecision") or "",
                    "checks": "fail" if bad else "pending" if pending else "pass" if checks else "none",
                    "author": (p.get("author") or {}).get("login", "")})
    return out


def prs(root):
    with ThreadPoolExecutor(6) as pool:
        return [p for rows in pool.map(prs_of, repo_dirs(root)) for p in rows]


if __name__ == "__main__":
    cmd, folder = sys.argv[1], sys.argv[2]
    data = {"sessions": lambda: sessions(folder, "--exact" in sys.argv),
            "repos": lambda: repos(folder), "prs": lambda: prs(folder)}[cmd]()
    json.dump({"at": int(time.time()), cmd: data}, sys.stdout, separators=(",", ":"))
