// A project's Home tab: logo and name, quick starts, recent Claude sessions to resume,
// its repos' git state and open pull requests, and its Paperclip link.
// It is a mod pane, so it never exits: the tab keeps the project (space) open even
// after every terminal in it has closed. Props: { space, folder, repos?, exact? }
//   repos: where to look for git repos (default: folder)
//   exact: list only sessions started in folder itself (for the home folder)
//   notes: the notes file (default: <folder>/NOTES.md; ~/Documents/omarchy-notes.md with exact)
// Brand details come from my-spaces through shared("brand.info"); data from ./home.py.
import { View, div, image, svg } from "gpui-kit";
import { v_flex, h_flex, Editor, EditorState } from "gpui-base";
import { props, spaces, agents, shared, theme, settings, run, exec, appHome, checking, readTextFile, writeTextFile } from "herdr";

const short = (path) => (path ?? "").replace(/^\/home\/[^/]+/, "~");
const clean = (s) => (s ?? "").replace(/^[^\p{L}\p{N}\p{Ps}\p{Pi}]+/u, "").trim();

function ago(seconds) {
  const m = Math.floor((Date.now() / 1000 - seconds) / 60);
  if (m < 1) return "now";
  if (m < 60) return `${m}m`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h`;
  const d = Math.floor(h / 24);
  return d < 30 ? `${d}d` : `${Math.floor(d / 30)}mo`;
}

export default class ProjectHome extends View {
  init(_props, cx) {
    this.data = { sessions: null, repos: null, prs: null };
    this.width = 900;
    // Notes: a markdown file in the project folder, so Claude sessions there can read it too.
    this.notes = EditorState.new({ language: "markdown", value: "", line_numbers: false, folding: false, soft_wrap: true,
      font_family: settings().font_family, font_size: 13 });
    this.saved = null; // the file's text as last read or written (null: no file yet)
    this.dirty = false;
    this.notes.on("change", () => { this.dirty = true; });
    if (checking()) return;
    this.loadNotes(cx);
    // Save a moment after typing stops; pick up edits made elsewhere when there are none here.
    cx.timer.every(1500, (cx) => this.saveNotes(cx));
    cx.timer.every(15000, (cx) => { if (!this.dirty) this.loadNotes(cx); });
    this.load(cx, "sessions");
    this.load(cx, "repos");
    this.load(cx, "prs");
    // Sessions and repos change as you work; pull requests are a network call, so slower.
    cx.timer.every(30000, (cx) => { this.load(cx, "sessions"); this.load(cx, "repos"); });
    cx.timer.every(300000, (cx) => this.load(cx, "prs"));
  }

  notesPath() {
    const p = props() ?? {};
    return p.notes ?? (p.exact ? "/home/kyle/Documents/omarchy-notes.md" : `${p.folder}/NOTES.md`);
  }

  loadNotes(cx) {
    cx.spawn(async (cx) => {
      const text = await readTextFile(this.notesPath()).catch(() => null);
      if (!this.dirty && text !== this.saved) {
        this.saved = text;
        this.notes.set_value(text ?? "");
        this.dirty = false;
        cx.notify();
      }
    });
  }

  saveNotes(cx) {
    if (!this.dirty || this.saving) return;
    const text = this.notes.value();
    if (text === (this.saved ?? "")) { this.dirty = false; return; }
    this.saving = true;
    this.dirty = false;
    cx.spawn(async (cx) => {
      try {
        await writeTextFile(this.notesPath(), text, this.saved);
        this.saved = text;
        this.notesError = null;
      } catch (e) {
        // Changed elsewhere since we read it: keep what's typed here, say so, re-read later.
        this.notesError = "Edited elsewhere at the same time; keeping your version";
        this.saved = await readTextFile(this.notesPath()).catch(() => this.saved);
        this.dirty = true;
      }
      this.saving = false;
      cx.notify();
    });
  }

  notesBox(t, color) {
    return v_flex().gap(4).min_w(0)
      .child(h_flex().h(22).gap(6).items_center().text_size(11).font_medium().text_color(t.dim)
        .child("NOTES").child(div().flex_1())
        .child(div().text_size(10.5).text_color(this.notesError ? t.blocked : t.dim)
          .child(this.notesError ?? this.notesPath().replace(/^\/home\/[^/]+/, "~"))))
      .child(div().h(200).rounded(8).border(1).border_color(color + "4d").bg(color + "0a").p(6).overflow_hidden()
        .child(Editor.new(this.notes)));
  }

  load(cx, what) {
    const p = props() ?? {};
    const folder = what === "sessions" ? p.folder : p.repos ?? p.folder;
    if (!folder) return;
    const args = ["-I", `${appHome()}/mods/Home/home.py`, what, folder, ...(what === "sessions" && p.exact ? ["--exact"] : [])];
    cx.spawn(async (cx) => {
      try {
        const r = await exec("python3", args, { timeout: 60000 });
        this.data[what] = JSON.parse(r.stdout)[what];
      } catch {
        this.data[what] ??= [];
      }
      cx.notify();
    });
  }

  button(id, icon, label, color, t, action) {
    return h_flex().id(id).h(30).px(12).gap(7).items_center().rounded(7).border(1).border_color(color + "66")
      .text_size(12.5).text_color(t.foreground).cursor_pointer()
      .hover((s) => s.bg(color + "26").border_color(color))
      .on_click(action)
      .child(svg(`mods/workspace-chrome/${icon}.svg`).size(13).flex_none().text_color(color))
      .child(label);
  }

  section(title, count, t, rows, empty) {
    return v_flex().gap(4).min_w(0)
      .child(h_flex().h(22).gap(6).items_center().text_size(11).font_medium().text_color(t.dim)
        .child(title.toUpperCase()).when(count != null, (el) => el.child(div().text_color(t.muted).child(String(count)))))
      .children(rows === null ? [div().text_size(12).text_color(t.dim).child("Loading…")]
        : rows.length ? rows : [div().text_size(12).text_color(t.dim).child(empty)]);
  }

  row(id, t, color, action) {
    return h_flex().id(id).h(28).px(8).gap(8).items_center().rounded(6).text_size(12.5).cursor_pointer()
      .hover((s) => s.bg(color + "1f")).on_click(action);
  }

  sessions(t, color, id, live) {
    const rows = this.data.sessions?.map((s) => {
      const open = live.get(s.title);
      return this.row(`s-${s.id}`, t, color, () => open
        ? run("pane.focus", { pane: open.pane })
        : run("tab.new", { space: id, folder: s.cwd, name: s.title.slice(0, 40), argv: ["claude", "--resume", s.id] }))
        .tooltip(`${s.title}\n${short(s.cwd)}\n${open ? "Open now: click to go there" : "Click to resume"}`)
        .child(svg("mods/workspace-chrome/square-pen.svg").size(12).flex_none().text_color(open ? color : t.dim))
        .child(div().flex_1().min_w(0).truncate().text_color(t.foreground).child(s.title))
        .when(Boolean(s.where), (el) => el.child(div().flex_none().max_w(150).truncate().text_size(11.5).text_color(t.dim).child(s.where)))
        .child(div().flex_none().w(34).text_right().text_size(11.5).text_color(open ? color : t.dim).child(open ? "open" : ago(s.at)));
    }) ?? null;
    return this.section("Recent sessions", null, t, rows, "No Claude sessions here yet");
  }

  repos(t, color, id) {
    const rows = this.data.repos?.map((r) => {
      const branch = r.branch && !["main", "master"].includes(r.branch) ? r.branch : "";
      return this.row(`r-${r.name}`, t, color, () => run("tab.new", { space: id, folder: r.path, name: r.name, argv: ["lazygit"] }))
        .tooltip(`${short(r.path)}\nbranch ${r.branch ?? "detached"}\nClick for lazygit`)
        .child(svg("mods/workspace-chrome/git-branch.svg").size(12).flex_none().text_color(t.dim))
        .child(div().flex_1().min_w(0).truncate().text_color(t.foreground).child(r.name))
        .when(Boolean(branch), (el) => el.child(div().flex_none().max_w(140).truncate().text_size(11.5).text_color(t.ansi4).child(branch)))
        .when(r.changed > 0, (el) => el.child(div().flex_none().text_size(11.5).text_color(t.ansi3).child(`${r.changed} changed`)))
        .when(r.ahead > 0, (el) => el.child(div().flex_none().text_size(11.5).text_color(t.ansi2).child(`↑${r.ahead}`)))
        .when(r.behind > 0, (el) => el.child(div().flex_none().text_size(11.5).text_color(t.ansi1).child(`↓${r.behind}`)))
        .when(!r.changed && !r.ahead && !r.behind, (el) => el.child(div().flex_none().text_size(11.5).text_color(t.dim).child("clean")));
    }) ?? null;
    return this.section("Repos", rows?.length ?? null, t, rows, "No git repos in this folder");
  }

  prs(t, color) {
    // Bots' dependency bumps go last and quiet; people's work first.
    const list = this.data.prs ? [...this.data.prs].sort((a, b) => (a.author.startsWith("app/") - b.author.startsWith("app/")) || b.number - a.number) : null;
    const mark = { pass: ["✓", t.ansi2], fail: ["✗", t.ansi1], pending: ["•", t.ansi3], none: ["·", t.dim] };
    const rows = list?.slice(0, 8).map((p) => {
      const [glyph, tone] = mark[p.checks] ?? mark.none;
      const bot = p.author.startsWith("app/");
      return this.row(`pr-${p.repo}-${p.number}`, t, color, () => exec("xdg-open", [p.url]))
        .tooltip(`${p.repo} #${p.number}\n${p.title}\nchecks ${p.checks}${p.review ? " · " + p.review.toLowerCase().replace("_", " ") : ""}${p.draft ? " · draft" : ""}`)
        .child(div().flex_none().w(12).text_color(tone).font_bold().child(glyph))
        .child(div().flex_none().text_size(11.5).text_color(t.dim).child(`#${p.number}`))
        .child(div().flex_1().min_w(0).truncate().text_color(bot || p.draft ? t.muted : t.foreground).child(p.title))
        .child(div().flex_none().max_w(140).truncate().text_size(11.5).text_color(t.dim).child(p.repo))
        .when(p.review === "APPROVED", (el) => el.child(div().flex_none().text_size(11).text_color(t.ansi2).child("approved")))
        .when(p.review === "CHANGES_REQUESTED", (el) => el.child(div().flex_none().text_size(11).text_color(t.ansi1).child("changes")));
    }) ?? null;
    const more = (list?.length ?? 0) > 8 ? [div().px(8).text_size(11.5).text_color(t.dim).child(`+${list.length - 8} more`)] : [];
    return this.section("Pull requests", list?.length ?? null, t, rows === null ? null : [...rows, ...more], "No open pull requests");
  }

  render() {
    const t = theme();
    const { space: id, folder } = props() ?? {};
    const space = spaces().find((s) => s.id === id);
    const brand = (shared("brand.info") ?? {})[id] ?? {};
    const color = /^#[0-9a-f]{6}$/i.test(brand.color ?? "") ? brand.color : t.accent.slice(0, 7);
    const name = space?.name ?? brand.name ?? "Project";
    const mine = agents().filter((a) => a.space === id);
    const live = new Map(mine.map((a) => [clean(a.title), a]));
    const count = (s) => mine.filter((a) => a.status === s).length;
    const busy = [["blocked", "need you"], ["done", "done"], ["working", "working"], ["idle", "idle"]]
      .filter(([s]) => count(s)).map(([s, label]) => `${count(s)} ${label}`).join(" · ");
    const start = (argv) => run("tab.new", { space: id, folder, ...(argv ? { argv } : {}) });
    const wide = this.width >= 820;

    const header = h_flex().gap(16).items_center().flex_wrap()
      .child(brand.logo
        ? image(brand.logo).size(52).rounded(12).flex_none()
        : h_flex().size(52).rounded(12).flex_none().bg(color).items_center().justify_center().text_size(24).font_bold().text_color("#ffffff").child([...name][0]?.toUpperCase() ?? "?"))
      .child(v_flex().gap(3).flex_1().min_w(200)
        .child(div().text_size(20).font_semibold().text_color(t.foreground).child(name))
        .child(h_flex().gap(10).text_size(12).text_color(t.dim)
          .child(short(folder))
          .child(div().text_color(busy ? color : t.dim).child(busy || "no agents running"))))
      .child(h_flex().gap(8).flex_wrap()
        .child(this.button("claude", "square-pen", "New Claude Code", color, t, () => start(["claude"])))
        .child(this.button("shell", "terminal", "Terminal", color, t, () => start(null)))
        .when(Boolean(brand.paperclip), (el) => el.child(this.button("paperclip", "layers", "Paperclip", color, t,
          () => exec("xdg-open", [brand.paperclip])))));

    const left = v_flex().gap(18).min_w(0).child(this.sessions(t, color, id, live)).child(this.notesBox(t, color));
    const right = v_flex().gap(18).min_w(0).child(this.repos(t, color, id)).child(this.prs(t, color));
    const body = wide
      ? h_flex().gap(28).items_start().child(left.flex_1()).child(right.flex_1())
      : v_flex().gap(18).child(left).child(right);

    return v_flex().id("home").size_full().bg(t.background).overflow_y_scroll()
      .on_size_change((size, cx) => { if (Math.abs(size.width - this.width) > 8) { this.width = size.width; cx.notify(); } })
      .child(v_flex().w_full().max_w(1100).mx_auto().px(28).py(26).gap(24)
        .child(header)
        .child(div().h(1).w_full().bg(color + "40"))
        .child(body)
        .child(div().text_size(11).text_color(t.dim).child("This tab keeps the project open when its terminals close.")));
  }
}
