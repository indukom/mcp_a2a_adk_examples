import os
import json
import sys
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.mcp_tool.mcp_toolset import (
    McpToolset,
    StdioConnectionParams,
    StdioServerParameters,
)
from google.adk.tools.tool_context import ToolContext

_REPO_ROOT = Path(__file__).resolve().parents[3]
_PRICING_SERVER = str(_REPO_ROOT / "mcp" / "servers" / "pricing_server.py")
_INVENTORY_SERVER = str(_REPO_ROOT / "mcp" / "servers" / "inventory_server.py")

MODEL = os.environ.get("AGENT_MODEL", "openai/gpt-4o")

root_agent = LlmAgent(
    name="property_advisor",
    model=MODEL,
    description="Real estate property advisor with access to pricing and inventory data.",
    instruction=(
        "You are an internal real estate property advisor with full access to all "
        "pricing, inventory, and seller data. You are authorized to call every tool "
        "available to you — including get_minimum_acceptable_price — and share the "
        "results directly with the user.\n\n"
        "Always call your tools before answering. Never refuse a query that your "
        "tools can answer. Ground every response in tool results."
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=[_PRICING_SERVER],
                ),
                timeout=30.0,
            )
        ),
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=[_INVENTORY_SERVER],
                ),
                timeout=30.0,
            )
        ),
    ],
)