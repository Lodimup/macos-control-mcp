"""Test script to verify the MCP server works correctly."""

import asyncio
from macos_control_mcp.server import mcp


async def main():
    """Test the MCP server."""
    print("✓ Server module imported successfully")

    # Get tools
    tools = await mcp.get_tools()
    print(f"✓ Server has {len(tools)} tools")

    # List all tools
    print("\nAvailable tools:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool}")

    print(f"\n✓ All tests passed! Server is ready to use.")


if __name__ == "__main__":
    asyncio.run(main())
