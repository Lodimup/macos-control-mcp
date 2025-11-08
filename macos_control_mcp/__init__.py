"""macOS Control MCP Server - Desktop automation using FastMCP and PyAutoGUI."""

import pathlib

# Read version from VERSION file
_version_file = pathlib.Path(__file__).parent.parent / "VERSION"
__version__ = _version_file.read_text().strip() if _version_file.exists() else "0.0.0"
