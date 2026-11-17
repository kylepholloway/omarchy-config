// Kyle's brands: which spaces get a logo instead of a letter tile.
// A space matches a brand when its name (or the folder its first terminal is in)
// contains one of `match`, or its folder is under `folder`. First match wins.
// `color` is the brand's primary (from its repo's tokens/logo); it outlines the
// selected project and its agent cards. Logos live next to this file in brands/ (72px rounded PNG tiles).
// Anything that matches nothing (or has no logo) keeps Herdr's colored letter tile.
// `paperclip`: the company's issues page; the project gets a link line to it (no polling, no keys).

export const BRANDS = [
  { name: "Holloway Network", logo: "holloway.png", color: "#F7A26A", folder: "Work/Holloway Network", match: ["holloway", "family-cookbook", "deploy-session"], paperclip: "https://agents.holloway.network/HOL/issues" },
  { name: "Archway", logo: "archway.png", color: "#6B8AFD", folder: "Work/Archway", match: ["archway"], paperclip: "https://agents.holloway.network/ARC/issues" },
  // No logo yet: keeps its letter tile and color, but gets its Paperclip line.
  { name: "Rockefeller", logo: null, color: null, folder: "Work/Rockefeller", match: ["rockefeller"], paperclip: "https://h2d.holloway.network/ROC/issues" },
  { name: "Nessi", logo: "nessi.png", color: "#6BAD99", folder: "Work/Nessi", match: ["nessi"] },
  { name: "SoCo", logo: "soco.png", color: "#CC3333", folder: "Work/SoCo", match: ["soco"] },
  { name: "Personal", logo: "personal.png", color: "#FF6A00", folder: "Work/Personal", match: ["ai-rag-portfolio", "portfolio", "kph"] },
];

const DIR = "mods/my-spaces/brands/";

// The brand for a space name and (optionally) a live folder, or null.
export function brandFor(name, folder) {
  const n = (name ?? "").toLowerCase();
  const f = (folder ?? "").toLowerCase();
  for (const b of BRANDS) {
    if (n === b.name.toLowerCase()) return b;
    if (b.match.some((m) => n.includes(m))) return b;
  }
  for (const b of BRANDS) {
    if (b.folder && f.includes("/" + b.folder.toLowerCase())) return b;
    if (b.match.some((m) => f.split("/").pop().includes(m))) return b;
  }
  return null;
}

export const logoPath = (b) => DIR + b.logo;
