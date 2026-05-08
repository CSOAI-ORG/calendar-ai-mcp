<div align="center">

# Calendar Ai MCP

**Calendar AI MCP Server — Schedule management tools.**

[![PyPI](https://img.shields.io/pypi/v/meok-calendar-ai-mcp)](https://pypi.org/project/meok-calendar-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Calendar AI MCP Server — Schedule management tools.

## Tools

| Tool | Description |
|------|-------------|
| `create_event` | Create a calendar event. start/end in ISO 8601 format (YYYY-MM-DDTHH:MM:SS). |
| `find_free_slot` | Find free time slots. busy_slots: JSON array of {start, end} objects. date: YYYY |
| `calculate_duration` | Calculate duration between two ISO 8601 datetime strings. |
| `timezone_convert` | Convert time between UTC offsets. Offsets in hours (e.g., -5 for EST, +1 for CET |

## Installation

```bash
pip install meok-calendar-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "calendar-ai": {
      "command": "python",
      "args": ["-m", "meok_calendar_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
