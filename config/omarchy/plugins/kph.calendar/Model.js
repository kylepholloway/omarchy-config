.pragma library

// Pure helpers for the calendar widget (no QML), so they can be tested with node.

var PROFILE_COLORS = {
  "Personal": "#9aa0a6",
  "Archway": "#6b8afd",
  "CAVA": "#f9d000",
  "TRF": "#00a19c"
}
var MAX_TITLE = 120
var MAX_EVENTS = 400

function colorFor(profile) {
  return PROFILE_COLORS[profile] || "#9aa0a6"
}

function clip(text, n) {
  text = String(text || "").replace(/\s+/g, " ").trim()
  return text.length > n ? text.slice(0, n - 1) + "…" : text
}

// Parse events.json text into validated, bounded event objects.
function parse(raw) {
  var data
  try { data = JSON.parse(raw) } catch (e) { return { events: [], errors: {}, updated: "" } }
  var list = Array.isArray(data && data.events) ? data.events.slice(0, MAX_EVENTS) : []
  var out = []
  for (var i = 0; i < list.length; i++) {
    var e = list[i] || {}
    var start = new Date(e.start), end = new Date(e.end)
    if (isNaN(start.getTime()) || isNaN(end.getTime())) continue
    var url = typeof e.joinUrl === "string" && /^https:\/\/[^\s]+$/.test(e.joinUrl) && e.joinUrl.length < 2000 ? e.joinUrl : ""
    out.push({
      profile: clip(e.profile, 24),
      title: clip(e.title, MAX_TITLE) || "(no title)",
      start: start,
      end: end,
      allDay: e.allDay === true,
      joinKind: ["zoom", "meet", "teams", "webex"].indexOf(e.joinKind) >= 0 ? e.joinKind : "",
      joinUrl: url
    })
  }
  out.sort(function(a, b) { return a.start - b.start })
  var errors = data && typeof data.errors === "object" && data.errors ? data.errors : {}
  return { events: out, errors: errors, updated: String(data && data.updated || "") }
}

function timed(events) {
  return events.filter(function(e) { return !e.allDay })
}

// The meeting happening now (latest started), else the next one today or later.
function current(events, now) {
  var live = timed(events).filter(function(e) { return e.start <= now && e.end > now })
  if (live.length) return live[live.length - 1]
  return null
}

function next(events, now) {
  var up = timed(events).filter(function(e) { return e.start > now })
  return up.length ? up[0] : null
}

// What to join from a hotkey or right-click: a live meeting, or one starting
// within the next 15 minutes.
function joinable(events, now) {
  var c = current(events, now)
  if (c && c.joinUrl) return c
  var n = next(events, now)
  if (n && n.joinUrl && n.start - now <= 15 * 60000) return n
  return c || null
}

function untilText(ms) {
  var m = Math.max(0, Math.round(ms / 60000))
  if (m < 1) return "now"
  if (m < 60) return m + "m"
  var h = Math.floor(m / 60), r = m % 60
  return r ? h + "h " + r + "m" : h + "h"
}

// The bar's BarIconButton is Omarchy-owned and may render rich text, so a
// meeting title must not reach it markup-shaped.
function noMarkup(text) {
  return String(text).replace(/</g, "‹").replace(/>/g, "›").replace(/&/g, "+")
}

// Bar label: live meeting, or the next one within 12 hours, else just the icon.
function label(events, now) {
  var c = current(events, now)
  if (c) return "󰃭  " + noMarkup(clip(c.title, 22)) + " · now"
  var n = next(events, now)
  if (n && n.start - now <= 12 * 3600000) return "󰃭  " + noMarkup(clip(n.title, 22)) + " · " + untilText(n.start - now)
  return "󰃭"
}

function dayKey(d) {
  return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate()
}

// Upcoming events grouped by day for the agenda: [{key, date, events}], at most `days` days.
function agenda(events, now, days) {
  var startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  var limit = new Date(startOfToday.getTime() + days * 86400000)
  var groups = [], byKey = {}
  events.forEach(function(e) {
    if (e.end <= now || e.start >= limit) return
    var day = e.start < startOfToday ? startOfToday : e.start
    var k = dayKey(day)
    if (!byKey[k]) {
      byKey[k] = { key: k, date: new Date(day.getFullYear(), day.getMonth(), day.getDate()), events: [] }
      groups.push(byKey[k])
    }
    byKey[k].events.push(e)
  })
  return groups
}
