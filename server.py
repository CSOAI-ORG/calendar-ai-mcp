"""Calendar AI MCP Server — Schedule management tools."""
import json
import time
from datetime import datetime, timedelta
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("calendar-ai-mcp")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    day_ago = now - 86400
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > day_ago]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

@mcp.tool()
def create_event(title: str, start: str, end: str, timezone: str = "UTC", description: str = "", attendees: str = "") -> dict[str, Any]:
    """Create a calendar event. start/end in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."""
    if not _rate_check("create_event"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        s = datetime.fromisoformat(start)
        e = datetime.fromisoformat(end)
    except ValueError:
        return {"error": "Invalid date format. Use ISO 8601: YYYY-MM-DDTHH:MM:SS"}
    if e <= s:
        return {"error": "End time must be after start time"}
    duration = (e - s).total_seconds()
    att_list = [a.strip() for a in attendees.split(",") if a.strip()] if attendees else []
    return {
        "event": {
            "title": title, "start": s.isoformat(), "end": e.isoformat(),
            "timezone": timezone, "description": description,
            "attendees": att_list, "duration_minutes": round(duration / 60, 1),
            "created_at": datetime.utcnow().isoformat()
        }
    }

@mcp.tool()
def find_free_slot(busy_slots: str, date: str, duration_minutes: int = 60, work_start: str = "09:00", work_end: str = "17:00") -> dict[str, Any]:
    """Find free time slots. busy_slots: JSON array of {start, end} objects. date: YYYY-MM-DD."""
    if not _rate_check("find_free_slot"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        slots = json.loads(busy_slots) if busy_slots else []
        base = datetime.fromisoformat(date)
    except (json.JSONDecodeError, ValueError) as e:
        return {"error": f"Invalid input: {e}"}
    ws_h, ws_m = map(int, work_start.split(":"))
    we_h, we_m = map(int, work_end.split(":"))
    day_start = base.replace(hour=ws_h, minute=ws_m, second=0)
    day_end = base.replace(hour=we_h, minute=we_m, second=0)
    busy = sorted([(datetime.fromisoformat(s["start"]), datetime.fromisoformat(s["end"])) for s in slots])
    free = []
    cursor = day_start
    for bs, be in busy:
        if bs > cursor and (bs - cursor).total_seconds() >= duration_minutes * 60:
            free.append({"start": cursor.isoformat(), "end": bs.isoformat(), "minutes": round((bs - cursor).total_seconds() / 60)})
        cursor = max(cursor, be)
    if cursor < day_end and (day_end - cursor).total_seconds() >= duration_minutes * 60:
        free.append({"start": cursor.isoformat(), "end": day_end.isoformat(), "minutes": round((day_end - cursor).total_seconds() / 60)})
    return {"date": date, "free_slots": free, "total_free_minutes": sum(s["minutes"] for s in free)}

@mcp.tool()
def calculate_duration(start: str, end: str) -> dict[str, Any]:
    """Calculate duration between two ISO 8601 datetime strings."""
    if not _rate_check("calculate_duration"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        s = datetime.fromisoformat(start)
        e = datetime.fromisoformat(end)
    except ValueError:
        return {"error": "Invalid date format"}
    delta = abs(e - s)
    total_sec = delta.total_seconds()
    return {
        "days": delta.days, "hours": int(total_sec // 3600),
        "minutes": int((total_sec % 3600) // 60), "seconds": int(total_sec % 60),
        "total_minutes": round(total_sec / 60, 1), "total_hours": round(total_sec / 3600, 2),
        "human_readable": f"{delta.days}d {int((total_sec%86400)//3600)}h {int((total_sec%3600)//60)}m"
    }

@mcp.tool()
def timezone_convert(datetime_str: str, from_offset: float, to_offset: float) -> dict[str, Any]:
    """Convert time between UTC offsets. Offsets in hours (e.g., -5 for EST, +1 for CET)."""
    if not _rate_check("timezone_convert"):
        return {"error": "Rate limit exceeded (50/day)"}
    try:
        dt = datetime.fromisoformat(datetime_str)
    except ValueError:
        return {"error": "Invalid datetime format"}
    diff = to_offset - from_offset
    converted = dt + timedelta(hours=diff)
    return {
        "original": dt.isoformat(), "converted": converted.isoformat(),
        "from_utc_offset": from_offset, "to_utc_offset": to_offset,
        "offset_difference_hours": diff
    }

if __name__ == "__main__":
    mcp.run()
