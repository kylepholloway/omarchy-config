import QtQuick
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Commons as Commons
import qs.Ui
import "Model.js" as Model

// Agenda popup for the merged calendar. Data comes from cal-sync
// (~/.cache/cal-sync/events.json); Join hands the link to webapp-profile so the
// meeting opens in the Chrome profile its calendar belongs to.
Panel {
  id: root
  moduleName: "kph.calendar"
  ipcTarget: "kph.calendar"
  manageIpc: false

  property var anchorItem: null
  property var hostWidget: null
  readonly property var barIdentity: hostWidget || root

  property var events: []
  property var errors: ({})
  property date now: new Date()
  readonly property string label: Model.label(events, now)
  readonly property var days: Model.agenda(events, now, 3)

  function openFromHotkey() {
    now = new Date()
    eventsFile.reload()
    root.controller.show()
  }
  function close() { root.controller.hide() }
  function toggle() { if (root.opened) root.close(); else root.openFromHotkey() }
  function switchPanel(direction) {
    if (root.bar && typeof root.bar.switchPanelFrom === "function")
      return root.bar.switchPanelFrom(root.barIdentity, direction)
    return false
  }

  function join(ev) {
    if (!ev || !ev.joinUrl) return
    Util.execArgv(["webapp-profile", "join", ev.profile, ev.joinUrl])
    root.close()
  }
  function joinNext() { join(Model.joinable(events, new Date())) }
  function syncNow() { Util.execArgv(["systemctl", "--user", "start", "cal-sync.service"]) }
  function openCalendarApp() { Util.execArgv(["omacal"]); root.close() }

  function timeText(ev) {
    if (ev.allDay) return "All day"
    var loc = Qt.locale(Commons.I18n.formatLocale)
    return ev.start.toLocaleTimeString(loc, "h:mm") + "–" + ev.end.toLocaleTimeString(loc, "h:mm AP")
  }
  function dayTitle(date) {
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    var diff = Math.round((date - today) / 86400000)
    var loc = Qt.locale(Commons.I18n.formatLocale)
    if (diff === 0) return "Today · " + date.toLocaleDateString(loc, "MMMM d")
    if (diff === 1) return "Tomorrow · " + date.toLocaleDateString(loc, "MMMM d")
    return date.toLocaleDateString(loc, "dddd · MMMM d")
  }

  FileView {
    id: eventsFile
    path: Quickshell.env("HOME") + "/.cache/cal-sync/events.json"
    watchChanges: true
    printErrors: false
    onFileChanged: reload()
    onLoaded: {
      var parsed = Model.parse(text())
      root.events = parsed.events
      root.errors = parsed.errors
    }
    onLoadFailed: { root.events = []; root.errors = ({}) }
  }

  // Keep the countdown fresh.
  Timer {
    interval: 30000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: root.now = new Date()
  }

  ShellIpc {
    target: root.ipcTarget
    function open(): void { root.openFromHotkey() }
    function close(): void { root.close() }
    function toggle(): void { root.toggle() }
    function joinNext(): void { root.joinNext() }
  }

  component Label: Text {
    textFormat: Text.PlainText
    color: root.bar ? root.bar.foreground : Commons.Color.foreground
    font.family: root.bar ? root.bar.fontFamily : Style.font.family
    font.pixelSize: Style.font.body
    elide: Text.ElideRight
  }

  KeyboardPanel {
    id: panel
    anchorItem: root.anchorItem
    owner: root.barIdentity
    bar: root.bar
    open: root.opened
    centerOnBar: false
    focusTarget: panel.loadedContent
    contentWidth: panel.fittedContentWidth(Style.space(420))
    contentHeight: panel.fittedContentHeight(panel.loadedContentHeight, Style.space(560))

    content: PanelKeyCatcher {
      anchors.fill: parent
      implicitHeight: agendaColumn.implicitHeight
      onCloseRequested: root.close()
      onReturnRequested: root.joinNext()
      onTabRequested: function(direction) { root.switchPanel(direction) }

      Flickable {
        id: scroller
        anchors.fill: parent
        contentWidth: width
        contentHeight: agendaColumn.implicitHeight
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        interactive: contentHeight > height

        Column {
          id: agendaColumn
          width: scroller.width
          spacing: Style.space(10)

          Label {
            visible: root.days.length === 0
            width: parent.width
            topPadding: Style.space(8)
            bottomPadding: Style.space(8)
            horizontalAlignment: Text.AlignHCenter
            opacity: 0.7
            text: Object.keys(root.errors).length
              ? "Couldn't reach: " + Object.keys(root.errors).join(", ")
              : "Nothing in the next three days"
          }

          Repeater {
            model: root.days

            Column {
              required property var modelData
              width: agendaColumn.width
              spacing: Style.space(4)

              Label {
                text: root.dayTitle(modelData.date)
                font.pixelSize: Style.font.bodySmall
                font.bold: true
                opacity: 0.6
                leftPadding: Style.space(4)
              }

              Repeater {
                model: modelData.events

                Rectangle {
                  id: row
                  required property var modelData
                  readonly property bool live: modelData.start <= root.now && modelData.end > root.now
                  readonly property bool past: modelData.end <= root.now
                  width: agendaColumn.width
                  height: Style.space(40)
                  radius: Style.space(6)
                  color: rowMouse.containsMouse && modelData.joinUrl
                    ? Style.hoverFillFor(root.bar.foreground, Commons.Color.accent)
                    : (live ? Qt.rgba(1, 1, 1, 0.06) : "transparent")
                  opacity: past ? 0.45 : 1

                  Rectangle {
                    id: dot
                    width: Style.space(4)
                    height: parent.height - Style.space(12)
                    radius: width / 2
                    anchors.left: parent.left
                    anchors.leftMargin: Style.space(6)
                    anchors.verticalCenter: parent.verticalCenter
                    color: Model.colorFor(row.modelData.profile)
                  }

                  Column {
                    anchors.left: dot.right
                    anchors.leftMargin: Style.space(10)
                    anchors.right: joinButton.visible ? joinButton.left : parent.right
                    anchors.rightMargin: Style.space(8)
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: Style.space(1)

                    Label {
                      width: parent.width
                      text: row.modelData.title
                      font.bold: row.live
                    }
                    Label {
                      width: parent.width
                      text: root.timeText(row.modelData) + "  ·  " + row.modelData.profile
                      font.pixelSize: Style.font.bodySmall
                      opacity: 0.65
                    }
                  }

                  Rectangle {
                    id: joinButton
                    visible: row.modelData.joinUrl !== "" && !row.past
                    anchors.right: parent.right
                    anchors.rightMargin: Style.space(8)
                    anchors.verticalCenter: parent.verticalCenter
                    width: joinText.implicitWidth + Style.space(18)
                    height: Style.space(24)
                    radius: height / 2
                    color: Model.colorFor(row.modelData.profile)

                    Label {
                      id: joinText
                      anchors.centerIn: parent
                      text: "Join"
                      color: "#111111"
                      font.pixelSize: Style.font.bodySmall
                      font.bold: true
                    }
                  }

                  MouseArea {
                    id: rowMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: row.modelData.joinUrl ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onClicked: if (row.modelData.joinUrl) root.join(row.modelData)
                  }
                }
              }
            }
          }

          Row {
            spacing: Style.space(16)
            leftPadding: Style.space(4)
            topPadding: Style.space(4)

            Label {
              text: "Open calendar"
              font.pixelSize: Style.font.bodySmall
              opacity: openMouse.containsMouse ? 1 : 0.6
              MouseArea { id: openMouse; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: root.openCalendarApp() }
            }
            Label {
              text: "Refresh"
              font.pixelSize: Style.font.bodySmall
              opacity: syncMouse.containsMouse ? 1 : 0.6
              MouseArea { id: syncMouse; anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor; onClicked: root.syncNow() }
            }
          }
        }
      }
    }
  }
}
