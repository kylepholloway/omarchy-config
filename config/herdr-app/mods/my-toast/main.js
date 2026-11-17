// How notifications look. Anything can post one with notify({ title, body,
// level, icon, action }); replace this mod to restyle them all. Click to
// run its action (e.g. go to the agent) and dismiss it.

import { View, div, image } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { props, closeOverlay, run, theme, window, exec, appHome, checking } from "herdr";

const DOT = { error: "blocked", warning: "working", success: "done", info: "accent" };

// While Herdr isn't the focused window, its notifications also go to Omarchy's own
// notification center (notify-send). Clicking one there runs the toast's action (usually:
// go to the agent) and brings Herdr forward. The in-app toast still shows as before.
export default class Toast extends View {
  init(_props, cx) {
    const p = props() ?? {};
    if (checking() || window()?.active) return;
    const icon = p.icon ? (p.icon.startsWith("/") ? p.icon : `${appHome()}/${p.icon}`) : "";
    const urgency = p.level === "error" ? "critical" : "normal";
    const args = ["-a", "Herdr", "-u", urgency, ...(icon && !icon.endsWith(".svg") ? ["-i", icon] : []),
      ...(p.action?.name ? ["-A", "default=Open"] : []), p.title ?? "Herdr", p.body ?? ""];
    cx.spawn(async (cx) => {
      // With an action, notify-send waits and prints "default" if the notification is clicked.
      const r = await exec("notify-send", args, { timeout: 600000 }).catch(() => null);
      if (r?.stdout?.trim() === "default" && p.action?.name) {
        run(p.action.name, p.action.args ?? {});
        await exec("hyprctl", ["dispatch", "focuswindow", "class:^(herdr-app)$"]).catch(() => null);
        closeOverlay(p.overlay);
      }
    });
  }

  render(cx) {
    const t = theme();
    const p = props() ?? {};
    const login = /^([a-z0-9][a-z0-9_.-]{0,31}) needs login; run hc machine login \1$/.exec(p.body ?? "");
    const command = login ? `hc machine login ${login[1]}` : null;
    return h_flex()
      .id("toast")
      .size_full()
      .px(18)
      .gap(12)
      .items_center()
      .bg(t.popover)
      .cursor_pointer()
      .hover((s) => s.bg(t.hover))
      .on_click(() => {
        if (p.action?.name) run(p.action.name, p.action.args ?? {});
        closeOverlay(p.overlay);
      })
      .child(p.icon ? image(p.icon).w(18).h(18).flex_none() : div().size(8).rounded(4).flex_none().bg(t[DOT[p.level] ?? "accent"]))
      .child(
        v_flex()
          .flex_1()
          .overflow_hidden()
          .child(div().truncate().font_semibold().text_size(13).text_color(t.foreground).child(login ? `${login[1]} needs a login: run` : p.title ?? ""))
          .when(!login && Boolean(p.body), (el) => el.child(div().truncate().text_size(12).text_color(t.muted).child(p.body ?? "")))
          .when(Boolean(login), (el) => el.child(h_flex().gap(8).items_center()
            .child(div().flex_1().min_w(0).truncate().tooltip(command).text_size(12).text_color(t.muted).child(command))
            .child(div().id("toast-login-copy").flex_none().px(6).py(3).rounded(4).bg(t.raised)
              .text_size(12).text_color(t.foreground).cursor_pointer().hover(s => s.bg(t.hover))
              .on_click((_e, cx) => { cx.stop_propagation(); cx.write_to_clipboard(command); this.copied = true; cx.notify(); })
              .child(this.copied ? "Copied" : "Copy")))),
      );
  }
}
