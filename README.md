# macOS Control MCP Server

A Model Context Protocol (MCP) server for macOS desktop automation using FastMCP and PyAutoGUI.

## Features

### Mouse Control
- Move mouse to coordinates
- Click (left, right, middle)
- Double-click
- Scroll
- Drag and drop
- Get mouse position

### Keyboard Control
- Type text
- Press individual keys
- Execute hotkey combinations (Cmd+C, Cmd+V, etc.)
- Hold and release keys

### Screen Capture & Analysis
- Take screenshots (full screen or regions)
- Get screen resolution
- Locate images on screen
- Get pixel colors at coordinates

### Utilities
- Sleep/pause execution
- Configure failsafe and pause settings

## Installation

### Prerequisites

- macOS
- Python 3.10 or later
- uv package manager

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd ~/macos-control-mcp
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Grant necessary permissions:**
   - **Accessibility Access**: System Settings → Privacy & Security → Accessibility
   - **Screen Recording**: System Settings → Privacy & Security → Screen Recording

   Add Terminal (or your terminal app) to both of these permissions.

### Configure Claude Desktop

Add this to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "macos-control": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/sb/macos-control-mcp",
        "run",
        "macos-control-mcp"
      ]
    }
  }
}
```

## Usage Examples

Once configured in Claude Desktop, you can use natural language to control your Mac:

### Mouse Control
- "Move the mouse to position 500, 300"
- "Click at coordinates 100, 200"
- "Double-click at the center of the screen"
- "Right-click at 400, 500"
- "Scroll down 5 clicks"

### Keyboard Control
- "Type 'Hello World'"
- "Press the Enter key"
- "Press Cmd+C to copy"
- "Press Cmd+Shift+3 to take a screenshot"

### Screen Capture
- "Take a screenshot"
- "What's the screen resolution?"
- "Get the color of the pixel at 100, 100"

### Combined Actions
- "Move mouse to 500, 300 and click"
- "Type 'test@example.com' and press Tab"
- "Press Cmd+Space, type 'Safari', and press Enter"

## Available Tools

### Mouse Tools
- `move_mouse(x, y, duration)` - Move cursor to coordinates
- `click_mouse(x, y, button, clicks, interval)` - Click at position
- `double_click(x, y)` - Double-click
- `right_click(x, y)` - Right-click
- `scroll_mouse(clicks, x, y)` - Scroll wheel
- `drag_mouse(x, y, duration, button)` - Drag to position
- `get_mouse_position()` - Get current cursor position

### Keyboard Tools
- `type_text(text, interval)` - Type text
- `press_key(key, presses, interval)` - Press a key
- `hotkey(*keys)` - Press key combination
- `key_down(key)` - Hold down a key
- `key_up(key)` - Release a key

### Screen Tools
- `get_screen_size()` - Get screen resolution
- `take_screenshot(region)` - Capture screen
- `locate_on_screen(image_path, confidence)` - Find image
- `get_pixel_color(x, y)` - Get RGB color

### Utility Tools
- `sleep(seconds)` - Pause execution
- `set_failsafe(enabled)` - Configure failsafe
- `set_pause(duration)` - Set action pause

## Safety Features

### Failsafe
By default, moving the mouse to any screen corner will abort PyAutoGUI operations. This can be disabled with `set_failsafe(False)`.

### Pause
A 0.1 second pause is inserted between actions by default. Adjust with `set_pause(duration)`.

## Development

### Running Tests
```bash
uv run pytest
```

### Running the Server Manually
```bash
uv run macos-control-mcp
```

## Troubleshooting

### "Permission denied" errors
Make sure you've granted Accessibility and Screen Recording permissions to your terminal application.

### "Image not found" errors
When using `locate_on_screen`, try lowering the confidence parameter (default is 0.9).

### Server not responding
1. Check Claude Desktop logs: `~/Library/Logs/Claude/`
2. Verify the path in your configuration matches your installation
3. Restart Claude Desktop

## License

MIT

## Credits

Built with:
- [FastMCP](https://github.com/jlowin/fastmcp) - Fast MCP server framework
- [PyAutoGUI](https://github.com/asweigart/pyautogui) - Cross-platform GUI automation
