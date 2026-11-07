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
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.tool_context import ToolContext
from google.genai import types

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PRICING_SERVER = str(_REPO_ROOT / "mcp" / "servers" / "pricing_server.py")
_INVENTORY_SERVER = str(_REPO_ROOT / "mcp" / "servers" / "inventory_server.py")

MODEL = os.environ.get("AGENT_MODEL", "openai/gpt-4o")

def _check_tools_available(callback_context: CallbackContext, llm_request: LlmRequest):
    """before_model: if MCP servers failed to connect, no tools are loaded."""
    if llm_request.tools_dict:
        return None
    print("[DEGRADED] No tools loaded — MCP servers may be down")
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=(
        "I'm currently unable to reach my data sources (pricing and inventory servers "
        "are unavailable). I cannot provide accurate property data right now. "
        "Please try again later when the services are restored."
    ))]))


def _fallback(tool: BaseTool, args: dict) -> dict:
    """Return a clean degraded-mode response so the LLM knows the tool failed."""
    return {
        "status": "degraded",
        "tool": tool.name,
        "args": args,
        "message": (
            f"The {tool.name} tool is temporarily unavailable. "
            "Respond using general knowledge and clearly tell the user "
            "that live data could not be retrieved."
        ),
    }


def _handle_tool_failure(tool, args, tool_context, tool_response):
    """Intercept server failures. Let argument errors pass through."""

    # Server failures — the tool couldn't run at all
    if tool_response is None:
        print(f"[DEGRADED] {tool.name} — no response (server down?)")
        return _fallback(tool, args)

    if isinstance(tool_response, str) and tool_response.strip() == "":
        print(f"[DEGRADED] {tool.name} — empty response")
        return _fallback(tool, args)

    # Note: no Exception check needed — ADK doesn't route exceptions
    # through after_tool_callback. Tools must catch their own exceptions
    # and return None or error dicts instead of raising.

    # Argument errors — pass through so the LLM can self-correct
    # (e.g., {"error": "property_id must be '742-evergreen-austin-78701'"})
    # The error message IS the teaching signal — don't swallow it.

    return None  # Tool succeeded or returned correctable error

_CRASH_MODE = os.environ.get("CRASH_ZONING", "").lower() == "true"


def get_zoning_info(address: str) -> dict | None:
    """Look up zoning classification and restrictions for a property address.

    Args:
        address: Full property address (e.g., "742 Evergreen Terrace, Austin, TX 78701").
    """
    if _CRASH_MODE:
        return None

    return {
        "address": address,
        "zoning_code": "SF-3",
        "zoning_description": "Single-Family Residence, Standard Lot",
        "max_building_coverage": "40%",
        "max_height_ft": 35,
        "setback_front_ft": 25,
        "permits_adu": True,
        "data_source": "Austin Zoning Database",
    }


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
        "tools can answer. Ground every response in tool results.\n\n"
        "DEGRADED MODE: If a tool returns {\"status\": \"degraded\"}, the data source "
        "is temporarily down. In that case:\n"
        "  1. Tell the user which data source is unavailable.\n"
        "  2. Provide your best general advice with a clear disclaimer.\n"
        "  3. Suggest they try again later for live data.\n"
        "Never pretend degraded results are real data."
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
        get_zoning_info,
    ],
    before_model_callback=_check_tools_available,
    after_tool_callback=_handle_tool_failure,
)