import QtQuick
import qs.Commons
import qs.Ui

// Bar pill for the merged calendar: shows the next meeting, opens the agenda.
// Modeled on omarchy.weather's BarWidget (panel loaded inside, bar identity
// forwarded so the popout coordinator treats this widget as the panel).
BarWidget {
  id: root
  moduleName: "kph.calendar"

  function injectPanel() {
    var target = panelLoader.item
    if (!target) return
    if ("bar" in target) target.bar = root.bar
    if ("settings" in target) target.settings = root.settings
    if ("anchorItem" in target) target.anchorItem = button
    if ("hostWidget" in target) target.hostWidget = root
  }

  readonly property bool opened: panelLoader.item ? panelLoader.item.opened === true : false
  function open() { if (panelLoader.item) panelLoader.item.openFromHotkey() }
  function close() { if (panelLoader.item) panelLoader.item.close() }
  readonly property bool popoutSwitchClosing: panelLoader.item ? panelLoader.item.popoutSwitchClosing === true : false
  function closeForPopoutSwitch() { if (panelLoader.item) panelLoader.item.closeForPopoutSwitch() }

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  onBarChanged: injectPanel()
  onSettingsChanged: injectPanel()

  Loader {
    id: panelLoader
    active: true
    source: Qt.resolvedUrl("Panel.qml")
    visible: false
    onLoaded: {
      root.injectPanel()
      Qt.callLater(root.injectPanel)
    }
  }

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: panelLoader.item ? panelLoader.item.label : "󰃭"
    tooltipText: ""

    onPressed: function(b) {
      if (!panelLoader.item) return
      if (b === Qt.MiddleButton) panelLoader.item.syncNow()
      else if (b === Qt.RightButton) panelLoader.item.joinNext()
      else panelLoader.item.toggle()
    }
  }
}
