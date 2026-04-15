# Calendar AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — Schedule management, free slot finding, and timezone conversion

## Installation

```bash
pip install calendar-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install calendar-ai-mcp
```

## Tools

### `create_event`
Create a calendar event with attendees and timezone support.

**Parameters:**
- `title` (str): Event title
- `start` (str): Start time in ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- `end` (str): End time in ISO 8601
- `timezone` (str): Timezone (default 'UTC')
- `description` (str): Event description
- `attendees` (str): Comma-separated attendee emails

### `find_free_slot`
Find free time slots in a day given busy periods.

**Parameters:**
- `busy_slots` (str): JSON array of {start, end} objects
- `date` (str): Date (YYYY-MM-DD)
- `duration_minutes` (int): Required duration (default 60)
- `work_start` (str): Work day start (default '09:00')
- `work_end` (str): Work day end (default '17:00')

### `calculate_duration`
Calculate duration between two ISO 8601 datetime strings.

**Parameters:**
- `start` (str): Start datetime
- `end` (str): End datetime

### `timezone_convert`
Convert time between UTC offsets.

**Parameters:**
- `datetime_str` (str): Datetime to convert
- `from_offset` (float): Source UTC offset in hours
- `to_offset` (float): Target UTC offset in hours

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
