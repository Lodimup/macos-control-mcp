# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server that enables macOS desktop automation through Claude Desktop. It uses FastMCP framework to expose PyAutoGUI automation capabilities as MCP tools.

**Core Architecture:**
- `macos_control_mcp/server.py` - Single-file MCP server implementation containing all tools
- FastMCP framework handles MCP protocol and tool registration via `@mcp.tool()` decorators
- PyAutoGUI provides cross-platform GUI automation primitives
- Server runs as subprocess spawned by Claude Desktop via `uv run macos-control-mcp`

## Development Commands

**Setup:**
```bash
uv sync                  # Install dependencies and create .venv
```

**Running:**
```bash
uv run macos-control-mcp        # Run the MCP server manually
uv run python tests/test_server.py  # Run basic server validation test
uv run pytest            # Run full test suite
```

**Python Version:**
- Uses Python 3.13 (specified in `.python-version`)
- Requires Python 3.10+ minimum

## Tool Categories

The server exposes 20 automation tools organized into 4 categories:

1. **Mouse Control** (7 tools): `move_mouse`, `click_mouse`, `double_click`, `right_click`, `scroll_mouse`, `drag_mouse`, `get_mouse_position`
2. **Keyboard Control** (5 tools): `type_text`, `press_key`, `hotkey`, `key_down`, `key_up`
3. **Screen Capture** (4 tools): `take_screenshot`, `get_screen_size`, `locate_on_screen`, `get_pixel_color`
4. **Utilities** (3 tools): `sleep`, `set_failsafe`, `set_pause`

## Important Implementation Details

**Screenshot Scaling:**
- `take_screenshot()` defaults to 25% scale (scale=0.25) to reduce data size
- **Critical:** Coordinates from screenshots must be multiplied by 4 for actual screen positions
- Example: Object at (100, 200) in screenshot is actually at (400, 800) on screen
- Can be overridden with `scale=1.0` for full resolution

**Safety Features:**
- PyAutoGUI failsafe enabled by default (move mouse to corner to abort operations)
- 0.1 second pause between actions via `pyautogui.PAUSE`
- Both configurable via `set_failsafe()` and `set_pause()` tools

**macOS Permissions Required:**
- Accessibility Access for mouse/keyboard control
- Screen Recording for screenshots and screen analysis
- Must be granted to Terminal (or whichever app runs the server)

## Testing

The test file `tests/test_server.py` is a basic validation script that:
- Verifies server module imports
- Checks all tools are registered
- Lists available tools

It does NOT perform functional testing of automation (would require GUI interaction).

## Claude Desktop Integration

Server is configured in `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "macos-control": {
      "command": "uv",
      "args": ["--directory", "<path_to_folder>/macos-control-mcp", "run", "macos-control-mcp"]
    }
  }
}
```

## Dependencies

Key dependencies (from `pyproject.toml`):
- `fastmcp>=0.2.0` - MCP server framework
- `pyautogui>=0.9.54` - GUI automation
- `pillow>=10.0.0` - Image processing for screenshots
- `opencv-python>=4.12.0.88` - Image recognition for `locate_on_screen`
- `pyobjc-framework-Quartz>=10.0` - macOS-specific screen APIs
- `pyobjc-framework-Cocoa>=10.0` - macOS-specific UI APIs
