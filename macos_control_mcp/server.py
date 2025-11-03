"""macOS Control MCP Server - Desktop automation using FastMCP and PyAutoGUI."""

import base64
import io
import time
from typing import Optional

import pyautogui
from fastmcp import FastMCP

# Configure PyAutoGUI safety features
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Short pause between actions

# Initialize FastMCP server
mcp = FastMCP("macos-control")


# ============================================================================
# MOUSE CONTROL TOOLS
# ============================================================================

@mcp.tool()
def move_mouse(x: int, y: int, duration: float = 0.2) -> str:
    """Move the mouse cursor to specific coordinates.

    Args:
        x: X coordinate (pixels from left)
        y: Y coordinate (pixels from top)
        duration: Time to move in seconds (default: 0.2)

    Returns:
        Success message with final position
    """
    pyautogui.moveTo(x, y, duration=duration)
    return f"Mouse moved to ({x}, {y})"


@mcp.tool()
def click_mouse(
    x: Optional[int] = None,
    y: Optional[int] = None,
    button: str = "left",
    clicks: int = 1,
    interval: float = 0.0
) -> str:
    """Click the mouse at current position or specified coordinates.

    Args:
        x: X coordinate (optional, uses current position if not specified)
        y: Y coordinate (optional, uses current position if not specified)
        button: Mouse button - "left", "right", or "middle" (default: "left")
        clicks: Number of clicks (default: 1)
        interval: Interval between clicks in seconds (default: 0.0)

    Returns:
        Success message
    """
    if x is not None and y is not None:
        pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
        return f"{button.capitalize()} clicked {clicks} time(s) at ({x}, {y})"
    else:
        pyautogui.click(clicks=clicks, interval=interval, button=button)
        pos = pyautogui.position()
        return f"{button.capitalize()} clicked {clicks} time(s) at current position ({pos.x}, {pos.y})"


@mcp.tool()
def double_click(x: Optional[int] = None, y: Optional[int] = None) -> str:
    """Double-click at current position or specified coordinates.

    Args:
        x: X coordinate (optional)
        y: Y coordinate (optional)

    Returns:
        Success message
    """
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
        return f"Double-clicked at ({x}, {y})"
    else:
        pyautogui.doubleClick()
        pos = pyautogui.position()
        return f"Double-clicked at current position ({pos.x}, {pos.y})"


@mcp.tool()
def right_click(x: Optional[int] = None, y: Optional[int] = None) -> str:
    """Right-click at current position or specified coordinates.

    Args:
        x: X coordinate (optional)
        y: Y coordinate (optional)

    Returns:
        Success message
    """
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
        return f"Right-clicked at ({x}, {y})"
    else:
        pyautogui.rightClick()
        pos = pyautogui.position()
        return f"Right-clicked at current position ({pos.x}, {pos.y})"


@mcp.tool()
def scroll_mouse(clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> str:
    """Scroll the mouse wheel.

    Args:
        clicks: Number of scroll clicks (positive = up, negative = down)
        x: X coordinate to scroll at (optional)
        y: Y coordinate to scroll at (optional)

    Returns:
        Success message
    """
    if x is not None and y is not None:
        pyautogui.scroll(clicks, x=x, y=y)
        return f"Scrolled {clicks} clicks at ({x}, {y})"
    else:
        pyautogui.scroll(clicks)
        pos = pyautogui.position()
        return f"Scrolled {clicks} clicks at ({pos.x}, {pos.y})"


@mcp.tool()
def drag_mouse(x: int, y: int, duration: float = 0.2, button: str = "left") -> str:
    """Drag the mouse from current position to target coordinates.

    Args:
        x: Target X coordinate
        y: Target Y coordinate
        duration: Time to drag in seconds (default: 0.2)
        button: Mouse button to hold - "left", "right", or "middle" (default: "left")

    Returns:
        Success message
    """
    start_pos = pyautogui.position()
    pyautogui.drag(x - start_pos.x, y - start_pos.y, duration=duration, button=button)
    return f"Dragged from ({start_pos.x}, {start_pos.y}) to ({x}, {y})"


@mcp.tool()
def get_mouse_position() -> str:
    """Get the current mouse cursor position.

    Returns:
        Current X and Y coordinates as a formatted string
    """
    pos = pyautogui.position()
    return f"Mouse position: ({pos.x}, {pos.y})"


# ============================================================================
# KEYBOARD CONTROL TOOLS
# ============================================================================

@mcp.tool()
def type_text(text: str, interval: float = 0.0) -> str:
    """Type text as if typing on the keyboard.

    Args:
        text: Text to type
        interval: Interval between keystrokes in seconds (default: 0.0)

    Returns:
        Success message
    """
    pyautogui.write(text, interval=interval)
    return f"Typed: {text[:50]}{'...' if len(text) > 50 else ''}"


@mcp.tool()
def press_key(key: str, presses: int = 1, interval: float = 0.0) -> str:
    """Press a specific key or key combination.

    Args:
        key: Key to press (e.g., 'enter', 'tab', 'esc', 'f1', 'shift', etc.)
        presses: Number of times to press (default: 1)
        interval: Interval between presses in seconds (default: 0.0)

    Returns:
        Success message
    """
    pyautogui.press(key, presses=presses, interval=interval)
    return f"Pressed '{key}' {presses} time(s)"


@mcp.tool()
def hotkey(keys: str) -> str:
    """Press a combination of keys simultaneously (e.g., Cmd+C, Cmd+V).

    Args:
        keys: Keys to press together, separated by '+' (e.g., 'command+c', 'command+shift+3')

    Returns:
        Success message

    Examples:
        - hotkey('command+c') - Copy
        - hotkey('command+v') - Paste
        - hotkey('command+shift+3') - Screenshot
    """
    key_list = [k.strip() for k in keys.split('+')]
    pyautogui.hotkey(*key_list)
    return f"Pressed hotkey: {keys}"


@mcp.tool()
def key_down(key: str) -> str:
    """Hold down a key (must call key_up to release).

    Args:
        key: Key to hold down

    Returns:
        Success message
    """
    pyautogui.keyDown(key)
    return f"Key '{key}' held down"


@mcp.tool()
def key_up(key: str) -> str:
    """Release a held key.

    Args:
        key: Key to release

    Returns:
        Success message
    """
    pyautogui.keyUp(key)
    return f"Key '{key}' released"


# ============================================================================
# SCREEN CAPTURE & INFORMATION TOOLS
# ============================================================================

@mcp.tool()
def get_screen_size() -> str:
    """Get the current screen resolution.

    Returns:
        Screen width and height
    """
    size = pyautogui.size()
    return f"Screen size: {size.width} x {size.height}"


@mcp.tool()
def take_screenshot(region: Optional[str] = None) -> str:
    """Take a screenshot of the entire screen or a specific region.

    Args:
        region: Optional region as "x,y,width,height" (e.g., "0,0,800,600")

    Returns:
        Base64 encoded PNG image data
    """
    if region:
        parts = [int(p.strip()) for p in region.split(',')]
        if len(parts) != 4:
            return "Error: Region must be in format 'x,y,width,height'"
        screenshot = pyautogui.screenshot(region=tuple(parts))
    else:
        screenshot = pyautogui.screenshot()

    # Convert to base64
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"


@mcp.tool()
def locate_on_screen(image_path: str, confidence: float = 0.9) -> str:
    """Locate an image on the screen and return its position.

    Args:
        image_path: Path to the image file to locate
        confidence: Match confidence (0.0 to 1.0, default: 0.9)

    Returns:
        Position of the image or error message if not found
    """
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            return f"Image found at: ({location.left}, {location.top}), size: {location.width}x{location.height}"
        else:
            return "Image not found on screen"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_pixel_color(x: int, y: int) -> str:
    """Get the RGB color of a pixel at specific coordinates.

    Args:
        x: X coordinate
        y: Y coordinate

    Returns:
        RGB color values
    """
    color = pyautogui.pixel(x, y)
    return f"Pixel at ({x}, {y}): RGB{color}"


# ============================================================================
# UTILITY TOOLS
# ============================================================================

@mcp.tool()
def sleep(seconds: float) -> str:
    """Pause execution for a specified duration.

    Args:
        seconds: Number of seconds to sleep

    Returns:
        Success message
    """
    time.sleep(seconds)
    return f"Slept for {seconds} seconds"


@mcp.tool()
def set_failsafe(enabled: bool) -> str:
    """Enable or disable PyAutoGUI failsafe (move mouse to corner to abort).

    Args:
        enabled: True to enable failsafe, False to disable

    Returns:
        Success message
    """
    pyautogui.FAILSAFE = enabled
    return f"Failsafe {'enabled' if enabled else 'disabled'}"


@mcp.tool()
def set_pause(duration: float) -> str:
    """Set the pause duration between PyAutoGUI actions.

    Args:
        duration: Pause duration in seconds

    Returns:
        Success message
    """
    pyautogui.PAUSE = duration
    return f"Pause set to {duration} seconds"


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
