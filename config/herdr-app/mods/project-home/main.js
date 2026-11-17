// A project's home tab: its logo and name, quick starts, and its Paperclip link.
// It is a mod pane, so it never exits: the tab keeps the project (space) open
// even after every terminal in it has closed. Props: { space, folder }.
// Brand details come from my-spaces through shared("brand.info").
import { View, div, image, svg } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { props, spaces, agents, shared, theme, run, exec } from "herdr";

const short = (path) => (path ?? "").replace(/^\/home\/[^/]+/, "~");

export default class ProjectHome extends View {
  button(id, icon, label, color, t, action) {
    return h_flex().id(id).h(34).px(14).gap(8).items_center().rounded(8).border(1).border_color(color + "66")
      .text_size(13).text_color(t.foreground).cursor_pointer()
      .hover((s) => s.bg(color + "26").border_color(color))
      .on_click(action)
      .child(svg(`mods/workspace-chrome/${icon}.svg`).size(14).flex_none().text_color(color))
      .child(label);
  }

  render() {
    const t = theme();
    const { space: id, folder } = props() ?? {};
    const space = spaces().find((s) => s.id === id);
    const brand = (shared("brand.info") ?? {})[id] ?? {};
    const color = /^#[0-9a-f]{6}$/i.test(brand.color ?? "") ? brand.color : t.accent.slice(0, 7);
    const name = space?.name ?? brand.name ?? "Project";
    const mine = agents().filter((a) => a.space === id);
    const count = (s) => mine.filter((a) => a.status === s).length;
    const busy = [["blocked", "need you"], ["done", "done"], ["working", "working"], ["idle", "idle"]]
      .filter(([s]) => count(s)).map(([s, label]) => `${count(s)} ${label}`).join(" · ");
    const start = (argv) => run("tab.new", { space: id, folder, ...(argv ? { argv } : {}) });
    return v_flex().size_full().bg(t.background).items_center().justify_center().gap(22).p(24)
      .child(v_flex().items_center().gap(12)
        .child(brand.logo
          ? image(brand.logo).size(64).rounded(14)
          : h_flex().size(64).rounded(14).bg(color).items_center().justify_center().text_size(30).font_bold().text_color("#ffffff").child([...name][0]?.toUpperCase() ?? "?"))
        .child(div().text_size(22).font_semibold().text_color(t.foreground).child(name))
        .child(div().text_size(12.5).text_color(t.dim).child(short(folder)))
        .child(div().text_size(12.5).text_color(t.muted).child(busy || "No agents running")))
      .child(h_flex().gap(10).flex_wrap().justify_center()
        .child(this.button("claude", "square-pen", "New Claude Code", color, t, () => start(["claude"])))
        .child(this.button("shell", "terminal", "New terminal", color, t, () => start(null)))
        .when(Boolean(brand.paperclip), (el) => el.child(this.button("paperclip", "layers", "Open in Paperclip", color, t,
          () => exec("xdg-open", [brand.paperclip])))))
      .child(div().text_size(11.5).text_color(t.dim).child("This tab keeps the project open when its terminals close."));
  }
}
