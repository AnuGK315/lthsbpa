#!/usr/bin/env python3
"""Sync the static homepage calendar from a public Google Calendar."""

from __future__ import annotations

import calendar
import html
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode, quote
from urllib.request import urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
CALENDAR_ID = "c605dc204f674a4d4a96296e7b42b155091bbbfa478b5b31d430d010be2d199d@group.calendar.google.com"
TIMEZONE = ZoneInfo("America/Chicago")


@dataclass
class Event:
    title: str
    start: datetime
    end: datetime
    location: str
    description: str
    all_day: bool
    color_id: str
    metadata_category: str


GOOGLE_COLOR_TO_CATEGORY = {
    "11": "Meetings",      # Tomato
    "6": "Events",         # Tangerine
    "2": "Conferences",    # Sage
    "7": "Deadlines",      # Peacock
}

CATEGORY_ALIASES = {
    "meeting": "Meetings",
    "meetings": "Meetings",
    "event": "Events",
    "events": "Events",
    "conference": "Conferences",
    "conferences": "Conferences",
    "deadline": "Deadlines",
    "deadlines": "Deadlines",
}


def parse_google_time(value: dict) -> tuple[datetime, bool]:
    if "dateTime" in value:
        raw = value["dateTime"].replace("Z", "+00:00")
        return datetime.fromisoformat(raw).astimezone(TIMEZONE), False

    day = date.fromisoformat(value["date"])
    return datetime.combine(day, time.min, TIMEZONE), True


def fetch_events(api_key: str, start: datetime, end: datetime) -> list[Event]:
    params = urlencode(
        {
            "key": api_key,
            "singleEvents": "true",
            "orderBy": "startTime",
            "maxResults": "80",
            "timeMin": start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "timeMax": end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
    )
    url = f"https://www.googleapis.com/calendar/v3/calendars/{quote(CALENDAR_ID, safe='')}/events?{params}"

    with urlopen(url, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    events: list[Event] = []
    for item in payload.get("items", []):
        if item.get("status") == "cancelled":
            continue
        start_dt, all_day = parse_google_time(item["start"])
        end_dt, _ = parse_google_time(item["end"])
        extended = item.get("extendedProperties", {})
        metadata_category = (
            extended.get("private", {}).get("category")
            or extended.get("shared", {}).get("category")
            or ""
        )
        events.append(
            Event(
                title=item.get("summary", "Untitled event"),
                start=start_dt,
                end=end_dt,
                location=item.get("location", ""),
                description=item.get("description", ""),
                all_day=all_day,
                color_id=item.get("colorId", ""),
                metadata_category=metadata_category,
            )
        )
    return events


def event_id(event: Event) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", event.title.lower()).strip("-")
    return f"{slug or 'event'}-{event.start.strftime('%Y%m%d')}"


def event_time(event: Event) -> str:
    if event.all_day:
        return "All day"
    start = event.start.strftime("%I:%M %p").lstrip("0").replace(":00", "")
    end = event.end.strftime("%I:%M %p").lstrip("0").replace(":00", "")
    return f"{start} - {end}"


def event_detail(event: Event) -> str:
    pieces = [f"{event.start.strftime('%b')} {event.start.day}", event_time(event)]
    if event.location:
        pieces.append(event.location)
    return " | ".join(pieces)


def event_category(event: Event) -> str:
    explicit_category = CATEGORY_ALIASES.get(event.metadata_category.strip().lower())
    if explicit_category:
        return explicit_category

    color_category = GOOGLE_COLOR_TO_CATEGORY.get(event.color_id)
    if color_category:
        return color_category

    text = f"{event.title} {event.description}".lower()
    if any(word in text for word in ["meeting", "chapter meeting", "sync", "check-in"]):
        return "Meetings"
    if any(word in text for word in ["conference", "regional", "state", "national"]):
        return "Conferences"
    if any(word in text for word in ["deadline", "due", "registration"]):
        return "Deadlines"
    return "Events"


def category_class(event: Event) -> str:
    return {
        "Meetings": "cat-meetings",
        "Events": "cat-events",
        "Conferences": "cat-conferences",
        "Deadlines": "cat-deadlines",
    }[event_category(event)]


def dot_class(event: Event) -> str:
    return {
        "Meetings": "tomato-dot",
        "Events": "tangerine-dot",
        "Conferences": "sage-dot",
        "Deadlines": "peacock-dot",
    }[event_category(event)]


def add_months(source: date, delta: int) -> date:
    month = source.month - 1 + delta
    year = source.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def render_day(day: date, month: int, events: list[Event], dot_offset: int) -> str:
    muted = " muted" if day.month != month else ""
    day_events = [event for event in events if event.start.date() == day]
    featured = " featured-day" if day_events and dot_offset == 0 else ""
    links = ""
    for event in day_events[:2]:
        links += f'<a class="calendar-event {category_class(event)}" href="#{event_id(event)}">{html.escape(event.title)}</a>'
    if len(day_events) > 2:
        links += f'<a class="calendar-event cat-events" href="#calendar-list">+{len(day_events) - 2} more</a>'
    return f'<div class="calendar-day{muted}{featured}"><span>{day.day}</span>{links}</div>'


def render_month(display_month: date, events: list[Event], panel_class: str) -> str:
    weeks = calendar.Calendar(firstweekday=6).monthdatescalendar(display_month.year, display_month.month)
    weekday_html = "".join(f'<div class="weekday">{name}</div>' for name in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    day_html = []
    event_days = sorted({event.start.date() for event in events})
    for week in weeks:
        for day in week:
            offset = event_days.index(day) if day in event_days else 99
            day_html.append(render_day(day, display_month.month, events, offset))
    month_label = display_month.strftime("%B %Y")
    return f"""<div class="month-panel {panel_class}" aria-label="{html.escape(month_label)} month calendar">
              {weekday_html}
              {"\n              ".join(day_html)}
            </div>"""


def render_event_list(events: list[Event]) -> str:
    if not events:
        return '<p class="empty-event">No events are currently listed on the chapter calendar.</p>'
    rows = []
    for event in events[:8]:
        rows.append(
            f'<article class="calendar-list-event {category_class(event)}" id="{event_id(event)}"><span class="event-dot {dot_class(event)}"></span>'
            f"<div><h4>{html.escape(event.title)}</h4><p>{html.escape(event_detail(event))}</p></div></article>"
        )
    return "\n            ".join(rows)


def render_milestones(events: list[Event]) -> str:
    if not events:
        return '<article><time><span>TBD</span>--</time><div><h3>No upcoming events</h3><p>Check back after the chapter calendar is updated.</p></div></article>'
    rows = []
    for index, event in enumerate(events[:3]):
        featured = ' class="featured"' if index == 0 else ""
        rows.append(
            f'<article{featured}><time><span>{event.start.strftime("%b")}</span>{event.start.strftime("%d").lstrip("0")}</time>'
            f"<div><h3>{html.escape(event.title)}</h3><p>{html.escape(event_detail(event))}</p></div></article>"
        )
    return "\n          ".join(rows)


def render_calendar(events: list[Event], display_month: date) -> str:
    categories = [
        ("filter-meetings", "Meetings", "tomato"),
        ("filter-events", "Events", "tangerine"),
        ("filter-conferences", "Conferences", "sage"),
        ("filter-deadlines", "Deadlines", "peacock"),
    ]
    filters = "\n                ".join(
        f'<label class="filter-chip {color}"><input class="category-filter" id="{filter_id}" type="checkbox"> {html.escape(category)}</label>'
        for filter_id, category, color in categories
    )
    month_label = display_month.strftime("%B %Y")
    prev_month = add_months(display_month, -1)
    next_month = add_months(display_month, 1)
    prev_events = [event for event in events if event.start.year == prev_month.year and event.start.month == prev_month.month]
    current_events = [event for event in events if event.start.year == display_month.year and event.start.month == display_month.month]
    next_events = [event for event in events if event.start.year == next_month.year and event.start.month == next_month.month]

    return f"""<!-- CALENDAR_SYNC_START -->
        <div class="calendar-shell event-manager reveal">
          <input class="view-radio" type="radio" name="calendar-view" id="view-month" checked>
          <input class="view-radio" type="radio" name="calendar-view" id="view-list">
          <input class="month-radio" type="radio" name="calendar-month" id="calendar-prev">
          <input class="month-radio" type="radio" name="calendar-month" id="calendar-current" checked>
          <input class="month-radio" type="radio" name="calendar-month" id="calendar-next">
          <div class="event-manager-top">
            <div>
              <p class="calendar-kicker">Chapter Calendar</p>
              <h3>
                <span class="month-title prev-title">{html.escape(prev_month.strftime("%B %Y"))}</span>
                <span class="month-title current-title">{html.escape(month_label)}</span>
                <span class="month-title next-title">{html.escape(next_month.strftime("%B %Y"))}</span>
              </h3>
            </div>
            <div class="calendar-actions" aria-label="Calendar month controls">
              <label class="icon-button" for="calendar-prev" aria-label="Previous month">&lt;</label>
              <label class="today-button" for="calendar-current">Current Month</label>
              <label class="icon-button" for="calendar-next" aria-label="Next month">&gt;</label>
            </div>
          </div>

          <div class="calendar-toolbar">
            <div class="search-field">
              <span aria-hidden="true">Search</span>
              <input type="search" placeholder="Static search field" aria-label="Search events">
            </div>
            <div class="view-toggle" aria-label="Calendar view">
              <label for="view-month">Month</label>
              <label for="view-list">List</label>
            </div>
            <details class="filter-menu">
              <summary>Filters</summary>
              <div class="filter-panel">
                {filters}
              </div>
            </details>
          </div>

          <div class="month-view">
            {render_month(prev_month, prev_events, "prev-panel")}
            {render_month(display_month, current_events, "current-panel")}
            {render_month(next_month, next_events, "next-panel")}
          </div>

          <div class="calendar-list-view" id="calendar-list" aria-label="Calendar event list">
            {render_event_list(events)}
          </div>
        </div>
        <!-- CALENDAR_SYNC_END -->"""


def replace_block(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.S)
    if not pattern.search(text):
        raise RuntimeError(f"Could not find generated block markers: {start_marker}")
    return pattern.sub(replacement, text)


def main() -> int:
    api_key = os.environ.get("GOOGLE_CALENDAR_API_KEY")
    if not api_key:
        print("Set GOOGLE_CALENDAR_API_KEY before running this script.", file=sys.stderr)
        return 2

    now = datetime.now(TIMEZONE)
    month_start = datetime(now.year, now.month, 1, tzinfo=TIMEZONE)
    range_start = datetime(add_months(date(now.year, now.month, 1), -1).year, add_months(date(now.year, now.month, 1), -1).month, 1, tzinfo=TIMEZONE)
    range_end = now + timedelta(days=365)
    events = fetch_events(api_key, range_start, range_end)
    upcoming = [event for event in events if event.end >= now]
    display_month = date(now.year, now.month, 1)

    html_text = INDEX_PATH.read_text(encoding="utf-8")
    html_text = replace_block(
        html_text,
        "<!-- CALENDAR_SYNC_START -->",
        "<!-- CALENDAR_SYNC_END -->",
        render_calendar(events, display_month),
    )
    html_text = replace_block(
        html_text,
        "<!-- MILESTONES_SYNC_START -->",
        "<!-- MILESTONES_SYNC_END -->",
        f"<!-- MILESTONES_SYNC_START -->\n          {render_milestones(upcoming)}\n          <!-- MILESTONES_SYNC_END -->",
    )
    INDEX_PATH.write_text(html_text, encoding="utf-8")
    print(f"Synced {len(events)} events from Google Calendar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
