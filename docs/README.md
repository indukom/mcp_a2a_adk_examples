# Real Estate Negotiation Workshop
## Learn MCP · A2A · Google ADK

A **4-hour hands-on workshop** teaching modern AI agent frameworks through a concrete, runnable project: an autonomous real estate negotiation between a Buyer Agent and a Seller Agent.

---

## What You'll Learn

| Concept | What It Is | How We Use It |
|---|---|---|
| **MCP** | Standard protocol for agents to access external tools | Agents query pricing/inventory servers via MCP |
| **A2A** | Agent-to-Agent protocol (Agent Card discovery + JSON-RPC over HTTP, task lifecycle, streaming) | Module 2 uses the true networked A2A protocol via `a2a-sdk` |
| **Google ADK** | Production-grade agent framework (LlmAgent, workflow agents, sessions, McpToolset, callbacks) | Module 2 builds the buyer and seller agents with ADK |

---

## The Scenario

**Property**: 742 Evergreen Terrace, Austin, TX 78701
*(4 BR / 3 BA / 2,400 sqft / Single Family / Built 2005)*

| Party | Goal | Starting Position | Walk-Away |
|---|---|---|---|
| **Buyer Agent** (GPT-4o) | Buy at lowest price | Offer $425,000 | Over $460,000 |
| **Seller Agent** (GPT-4o) | Sell at highest price | Counter $477,000 | Below $445,000 |

The negotiation runs for a maximum of **5 rounds**. Agents use real market data (via MCP) to justify every offer.

---

## Project Structure

Folders are numbered in teaching order. Each module introduces one new concept.

```
mcp_a2a_gcp_practice/
│
├── mcp/                               # MODULE 1 — External data via MCP
│   ├── README.md                      # Module guide for learners
│   ├── servers/
│   │   ├── pricing_server.py          # Custom MCP: market pricing tools
│   │   └── inventory_server.py        # Custom MCP: inventory + seller constraints
│   ├── clients/
│   │   ├── github_agent_client.py     # LLM agent that calls GitHub tools via MCP
│   │   └── sse_agent_client.py        # SSE agent client (LLM picks tools over HTTP)
│   ├── demos/                         # Standalone deep-dive demos (handshake, tool loop, primitives, content types, HTTP transport)
│   ├── exercises/                     # Hands-on coding exercises for Module 1
│   ├── solutions/                     # Worked solutions for Module 1 exercises
│   └── notes/
│       └── mcp_deep_dive.md           # Reference: MCP protocol deep dive
│
├── adk/                               # MODULE 2 — Google ADK
│   ├── README.md                      # Module guide for learners
│   ├── negotiation_agents/            # adk web-launchable agent packages
│   │   ├── buyer_agent/agent.py       # Buyer LlmAgent + McpToolset (pricing)
│   │   ├── seller_agent/agent.py      # Seller LlmAgent + McpToolset (pricing + inventory)
│   │   └── negotiation/agent.py       # LoopAgent + SequentialAgent + MCP tools + submit_decision
│   ├── demos/                         # adk web-launchable demos (d01–d09)
│   ├── exercises/                     # Hands-on coding exercises for Module 2
│   ├── solutions/                     # Worked solutions for Module 2 exercises
│   └── notes/
│       ├── a2a_protocols.md           # Reference: A2A protocol deep dive
│       ├── adk_quick_reference.md     # Reference: ADK API quick reference
│       └── google_adk_overview.md     # Reference: Google ADK overview
│
├── a2a/                               # A2A protocol demos & agents
│   ├── demos/                         # A2A terminal scripts (10–14), run against adk web --a2a
│   │   ├── a2a_10_wire_lifecycle.py   # Agent Card + the HTTP bytes of message/send + the Task
│   │   ├── a2a_11_context_threading.py    # contextId across rounds; taskId vs contextId
│   │   ├── a2a_12_parts_and_artifacts.py  # multi-part messages; history vs artifacts
│   │   ├── a2a_13_orchestrated_negotiation.py  # buyer↔seller negotiation: buyer polled, seller streamed
│   │   └── a2a_14_error_handling.py   # transport / protocol / task / application errors
│   └── resilient_advisor/             # Resilient multi-server agent
│
├── gcp/                               # GCP practice exercises
│   ├── ex_01_basic_agent/             # Basic LlmAgent + function tool
│   ├── ex_02_mcp_tools/              # McpToolset + auth
│   └── ex_03_session_state/          # Sessions & state scopes
│
├── docs/                              # Workshop slide deck (97 slides)
├── utils/
│   └── pricing_auth.py                # Demo JWTs for the pricing server's --http mode: mint (CLI) + verify
├── .env.example                       # Copy to .env and add your API keys
└── requirements.txt
```

If module files feel overwhelming, start with the README inside each module folder.

### Deep-dive demos

Modules 1 and 2 ship a `demos/` folder of small, single-purpose, runnable scripts that crack open the protocols on the wire — designed to pair with the `notes/` reference docs. See each module README for the per-demo table:

- [mcp/demos/](mcp/demos/) — MCP handshake, tool loop trace, primitives, content types, Streamable HTTP
- [adk/demos/](adk/demos/) — ADK concept demos (basic agent, MCP tools, sessions, sequential, parallel, loop, agent-as-tool, callbacks, event stream)
- [a2a/demos/](a2a/demos/) — A2A protocol scripts (wire format, context threading, parts/artifacts, orchestrated negotiation with polling/streaming, error handling)

### Notes live inside each module

Each module has a `notes/` subfolder with reference documentation. There are
two flavors: **demo study notes** (read while running the demos, narrate
expected output and key observations) and **conceptual deep-dives** (read any
time after the workshop for the theory and production patterns).

Every note has a header block stating its audience, prerequisites, what to
read before/after it, and a 3-point TL;DR. Open any note — the first thing
you'll see is whether it's the right one for you right now.

#### Recommended reading order

| When | Read | Why |
|---|---|---|
| **While running M1 demos** | [`mcp/notes/M1_DEMO_STUDY_NOTES.md`](mcp/notes/M1_DEMO_STUDY_NOTES.md) | Per-demo narration of all 5 MCP demos plus the GitHub + SSE clients |
| **After M1** | [`mcp/notes/mcp_deep_dive.md`](mcp/notes/mcp_deep_dive.md) | Full MCP protocol reference — primitives, transports, design patterns |
| **While running M2 demos** | [`adk/notes/M2_DEMO_STUDY_NOTES.md`](adk/notes/M2_DEMO_STUDY_NOTES.md) | Per-demo narration of all 9 ADK demos + the A2A demos (10–14) + the negotiation system |
| **After M2 (start here)** | [`adk/notes/adk_quick_reference.md`](adk/notes/adk_quick_reference.md) | One-page lookup for every ADK + A2A construct |
| **After M2 (go deep)** | [`adk/notes/google_adk_overview.md`](adk/notes/google_adk_overview.md) | Full ADK reference — every agent type, callbacks, sessions, event stream |
| **After M2 (network layer)** | [`adk/notes/a2a_protocols.md`](adk/notes/a2a_protocols.md) | Full A2A reference — wire format, contextId, parts, artifacts, streaming, production patterns |

Module 2 has three notes because it spans two distinct topics: the A2A protocol standard and the ADK runtime. Read `adk_quick_reference.md` first to get the construct names in your head; reach for the other two when you need depth on a specific construct.

---

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Node.js 18+ (optional — only for the MCP Inspector GUI in Module 1)

**Verify installation:**
```bash
python --version  # should be 3.10+
node --version    # optional: 18+ for the MCP Inspector
```

### 2. Clone or open this repo

```bash
# If you already have the repo, skip this step
git clone <your-repo-url>
cd mcp_a2a_gcp_practice
```

### 3. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
```

**macOS/Linux:**
```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

**Windows (PowerShell):**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bat
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

> **Tip**: Your prompt will change to show `(.venv)` when the environment is active.
> To deactivate at any time, run `deactivate`.

### 5. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs Google ADK 2.x. The first time you run an `adk` command (e.g. `adk web`), it asks **"Enable telemetry? [Y/n]"** — pressing Enter answers *yes*. Type `n` to decline, or run `adk telemetry disable` beforehand; the choice is saved in `~/.adk/config.json` and you won't be asked again. (The question only appears in an interactive terminal.)

### 6. Configure API keys

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

Then edit `.env` and set:
```env
OPENAI_API_KEY=sk-your-key-here
GITHUB_TOKEN=ghp-your-token-here   # Optional — Module 1 GitHub demo only
```

### 7. Run a smoke test

```bash
# Smoke test — run the MCP pricing server standalone
python mcp/servers/pricing_server.py
```

If it runs cleanly, your Python environment is ready.

### 8. Run the Workshop Modules in Order

```bash
# MODULE 1: MCP protocol
python mcp/clients/github_agent_client.py      # GitHub MCP agent (needs GITHUB_TOKEN + OPENAI_API_KEY)
python mcp/servers/pricing_server.py           # Run MCP server standalone (stdio)
python mcp/servers/pricing_server.py --sse --port 8001  # SSE transport mode
python mcp/servers/pricing_server.py --http             # Streamable HTTP + JWT auth (needed by ADK demo d02)
python utils/pricing_auth.py --role buyer --write-env   # mint a token for d02 (buyer | analyst | guest)
# MCP deep-dive demos (no API key needed unless noted):
python mcp/demos/01_initialize_handshake.py
python mcp/demos/02_tool_loop_trace.py
python mcp/demos/03_list_all_primitives.py
python mcp/demos/04_content_types.py
python mcp/demos/05_streamable_http_transport.py

# MODULE 2: Google ADK + A2A protocol (needs OPENAI_API_KEY)
adk web adk/demos/               # ADK demos d01–d09 in dropdown
python adk/demos/d09_event_stream/run_event_stream.py  # d09 in the terminal: print every ADK Event
adk web adk/negotiation_agents/       # buyer, seller, negotiation in dropdown
adk web --a2a adk/negotiation_agents/ # same + A2A endpoints + Agent Cards
# A2A protocol demos (run in a second terminal against adk web --a2a):
python a2a/demos/a2a_10_wire_lifecycle.py --seller-url http://127.0.0.1:8000/a2a/seller_agent
python a2a/demos/a2a_11_context_threading.py --seller-url http://127.0.0.1:8000/a2a/seller_agent
python a2a/demos/a2a_12_parts_and_artifacts.py --seller-url http://127.0.0.1:8000/a2a/seller_agent
# A2A orchestrated negotiation — buyer polled, seller streamed (via Agent Cards):
python a2a/demos/a2a_13_orchestrated_negotiation.py
# Error handling at four layers:
python a2a/demos/a2a_14_error_handling.py
```

### 9. Module Exercises

Module 1 and Module 2 ship hands-on exercises with complete, runnable solutions. **These are designed for the 2-hour follow-up review session** held a few days after the workshop — students attempt them as homework, the instructor walks through each solution and runs it live in class.

| Module | Exercise | Difficulty | Task |
|---|---|---|---|
| M1 | `ex01_walk_score_tool.md` | `[Starter]` | Add a `get_walk_score` tool to the pricing server; watch the LLM auto-discover and use it |
| M1 | `ex02_multi_server_agent.md` | `[Core]` | Build an `LlmAgent` that connects to both pricing + inventory MCP servers from scratch |
| M2 | `ex01_budget_cap_callback.md` | `[Starter]` | Write a `before_tool_callback` that blocks `submit_decision` calls with `price > $460,000` |
| M2 | `ex02_stuck_detection.md` | `[Core]` | Modify the orchestrator to track offer history and escalate early when rounds stall |
| M2 | `ex03_a2a_multiround_client.md` | `[Core]` | Write an A2A client that drives buyer ↔ seller via `message/send` with `contextId` threading |
| M2 | `ex04_mediator_agent.md` | `[Core]` | Build a mediator that wraps buyer + seller as `AgentTool`s and proposes a midpoint |
| M2 | `ex05_prompt_injection_defense.md` | `[Core]` | Add a `before_model_callback` to detect and redact prompt injection attempts |
| M2 | `ex06_human_in_the_loop.md` | `[Core]` | Add a human-approval checkpoint with three-tier governance: auto-approve, checkpoint, block |
| M2 | `ex07_parallel_negotiation.md` | `[Stretch]` | Negotiate with two sellers in parallel using `ParallelAgent`, then pick the best deal |
| M2 | `ex08_shared_market_intel.md` | `[Core]` | Use `app:` state as shared market intelligence — cache pricing lookups for all agents |
| M2 | `ex09_adaptive_strategy.md` | `[Stretch]` | Episodic memory + strategy advisor `AgentTool` that analyses concession patterns |

Each solution lives in its module's `solutions/` folder as a self-contained, runnable package — `agent.py` files you can launch directly with `adk web`, or scripts you can run with `python`. The instructor walks through each solution live during the review session.

---

## Module Run Reference

One-line summary of every runnable file in the workshop, grouped by module. Use this as a quick lookup or as slide content.

### Module 1 — MCP (give agents real tools)

| # | Run | What it means (one line) |
|---|---|---|
| 1 | `python mcp/clients/github_agent_client.py` | LLM agent talks to **GitHub's official hosted MCP server** over Streamable HTTP — lists tools, resource templates and prompts, attaches a repo README as a resource, and runs the ReAct tool loop on a familiar API. |
| 2 | `python mcp/servers/pricing_server.py` *(or `--sse --port 8001`)* | Custom MCP server exposing `get_market_price` + `calculate_discount` — the buyer/seller's source of market data. |
| 3 | `python mcp/servers/inventory_server.py` *(or `--sse --port 8002`)* | Custom MCP server with `get_inventory_level` (public) + `get_minimum_acceptable_price` (seller-only) — demonstrates **information asymmetry**. |
| 4 | `python mcp/clients/sse_agent_client.py` *(after starting servers in SSE mode)* | Same agent loop as the GitHub client, but over **HTTP/SSE** — proves the transport is irrelevant. |
| 5 | `python mcp/demos/01_initialize_handshake.py` | Raw JSON-RPC frames of the MCP `initialize` handshake — see the protocol on the wire, no SDK. |
| 6 | `python mcp/demos/02_tool_loop_trace.py` | Full **model ↔ host ↔ server** tool-calling loop, narrated step-by-step with timestamps. |
| 7 | `python mcp/demos/03_list_all_primitives.py` | Lists **Tools, Resources, and Prompts** from both servers — proves MCP carries more than just tools. |
| 8 | `python mcp/demos/04_content_types.py` | Inline server returning each Content block kind (text / image / embedded resource) so you see the JSON shapes. |
| 9 | `python mcp/demos/05_streamable_http_transport.py --serve` *(then `--client`)* | Same MCP protocol over **Streamable HTTP** — the spec's recommended replacement for raw SSE. |

### Module 2 — Google ADK + A2A (multi-agent orchestration)

**ADK demos — interactive Web UI** (`adk web adk/demos/`)

| # | Pick from dropdown | What it means (one line) |
|---|---|---|
| d01 | `d01_basic_agent` | Bare `LlmAgent` + a Python function tool — the simplest possible ADK agent. |
| d02 | `d02_mcp_tools` | `LlmAgent` + `McpToolset` over Streamable HTTP — connects to `pricing_server.py --http` with a JWT and discovers its tools; shows authentication (401), server authorization (403) and tool-level scopes. Start the server and mint a token first. |
| d03 | `d03_sessions_state` | `ToolContext` state at three scopes — session (this conversation), `user:` (this user), and `app:` (everyone). |
| d04 | `d04_sequential` | `SequentialAgent` pipeline — each step's `output_key` feeds the next via `{placeholder}`. |
| d05 | `d05_parallel` | `ParallelAgent` fan-out — concurrent agents writing to different state keys. |
| d06 | `d06_loop` | `LoopAgent` that iterates until a callback sets `actions.escalate = True`. |
| d07 | `d07_agent_as_tool` | `AgentTool` — wrap a whole agent as a callable tool for hierarchical delegation. |
| d08 | `d08_callbacks` | Five hooks enforcing policy the prompt doesn't state — `before_agent` (turn count), `before_model` (SSN redaction), `before_tool` (allowlist block), `after_tool` (strip a confidential field), `after_model` (scrub phone numbers from replies). |
| d09 | `d09_event_stream` | Inspect ADK's event stream — tool calls, state deltas, final-response markers. Terminal version: `python adk/demos/d09_event_stream/run_event_stream.py` prints every `Event` from `Runner.run_async()`. |

**A2A protocol demos — terminal scripts** (start `adk web --a2a adk/negotiation_agents/` first)

| # | Run | What it means (one line) |
|---|---|---|
| 10 | `python a2a/demos/a2a_10_wire_lifecycle.py --seller-url …/a2a/seller_agent` | Agent Card discovery, the actual HTTP request/response of `message/send`, and the returned **Task** taken apart (id, contextId, status, history, artifacts). |
| 11 | `python a2a/demos/a2a_11_context_threading.py --seller-url …/a2a/seller_agent` | Reuse `contextId` across rounds — multiple A2A calls become **one threaded conversation**; each round is a new Task (`tasks/get` fetches any of them). |
| 12 | `python a2a/demos/a2a_12_parts_and_artifacts.py --seller-url …/a2a/seller_agent` | Multi-part Messages (`TextPart` + `DataPart`); where content lives in a Task — history (tool calls as DataParts), status message, **Artifacts**. |
| 13 | `python a2a/demos/a2a_13_orchestrated_negotiation.py` | Full **buyer ↔ seller multi-round negotiation** over A2A — the client reads each card: buyer **polled** (`tasks/get`), seller **streamed** (`message/stream`). |
| 14 | `python a2a/demos/a2a_14_error_handling.py` | **Error handling** at four layers: transport and protocol errors raise; a `failed` task and a useless `completed` answer don't — check the state and the content. |

**Negotiation agents — interactive Web UI** (`adk web adk/negotiation_agents/`)

| Pick from dropdown | What it means (one line) |
|---|---|
| `buyer_agent` | `LlmAgent` + pricing `McpToolset`; `before_tool_callback` enforces allowlist (cannot see seller's floor). |
| `seller_agent` | `LlmAgent` + **two** `McpToolset`s (pricing + inventory) — has private access to `get_minimum_acceptable_price`. |
| `negotiation` | `LoopAgent` wrapping `SequentialAgent(buyer → seller)` — agreement detected via a structured `submit_decision` tool, not free text. |

---

## Architecture Deep Dive

### ADK + A2A Flow

```
adk web --a2a adk/negotiation_agents/
    │
    ├── buyer_agent (negotiation_agents/buyer_agent/agent.py)
    │     ├── root_agent = LlmAgent(model=AGENT_MODEL)  # default: openai/gpt-4o
    │     └── McpToolset → mcp/servers/pricing_server.py
    │
    ├── seller_agent (negotiation_agents/seller_agent/agent.py)
    │     ├── root_agent = LlmAgent(model=AGENT_MODEL)  # default: openai/gpt-4o
    │     ├── McpToolset → mcp/servers/pricing_server.py
    │     └── McpToolset → mcp/servers/inventory_server.py (seller ONLY)
    │
    └── negotiation (negotiation_agents/negotiation/agent.py)
          └── root_agent = LoopAgent(sub_agents=[SequentialAgent(buyer, seller)])

A2A endpoints (cards from each agent.json):
  GET  /a2a/buyer_agent/.well-known/agent-card.json     (streaming: false → poll tasks/get)
  POST /a2a/buyer_agent                                 (message/send)
  GET  /a2a/seller_agent/.well-known/agent-card.json    (streaming: true)
  POST /a2a/seller_agent                                (message/send, message/stream)
  GET  /a2a/negotiation/.well-known/agent-card.json
  POST /a2a/negotiation                                 (message/send)
```

### MCP Data Flow

```
BUYER AGENT                     MCP Protocol                PRICING SERVER
──────────────────────          ─────────────────────       ──────────────────
"I need market data"
await call_tool(
  "get_market_price",    ──►   tools/call request    ──►   Executes Python fn
  {"address": "742..."}) ◄──   CallToolResult        ◄──   Returns dict
"Comps avg $462K,
 listing is 4.9% above
 market. I'll offer
 $425K."
```

### A2A Message Exchange

```
Round 1: BUYER  ──[OFFER: $425,000]──────────────────────────────► SELLER
Round 1: BUYER ◄──[COUNTER_OFFER: $477,000]───────────────────── SELLER
Round 2: BUYER  ──[OFFER: $438,000]──────────────────────────────► SELLER
Round 2: BUYER ◄──[COUNTER_OFFER: $465,000]───────────────────── SELLER
Round 3: BUYER  ──[OFFER: $449,000]──────────────────────────────► SELLER
Round 3: BUYER ◄──[ACCEPT: $449,000]──────────────────────────── SELLER
                   ✅ DEAL REACHED at $449,000
                   (Buyer saved $36,000 from listing price)
```

---

## Workshop Schedule (4 Hours)

The full 97-slide deck ships as a PDF in the repo root.

| Time | Module | Topic | Key Files |
|---|---|---|---|
| 0:00–0:15 | Intro | What we're building | `README.md` |
| 0:15–1:00 | M1 | MCP with GitHub | `mcp/clients/github_agent_client.py` |
| 1:30–2:15 | M1 | MCP deep dive: protocol, primitives, transports, custom servers | `mcp/notes/mcp_deep_dive.md`, `mcp/servers/pricing_server.py` |
| 2:15–3:00 | M2 | Google ADK deep dive: LlmAgent, workflow agents, sessions, callbacks | `adk web adk/demos/` |
| 3:00–3:50 | M2 | A2A protocol: Agent Card, JSON-RPC, task lifecycle | `adk web --a2a adk/negotiation_agents/` |
| 3:50–4:00 | Wrap | Q&A + preview of follow-up exercise session | `mcp/exercises/`, `adk/exercises/` |

---

## Running the MCP Servers Manually

### Inspect Available Tools

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def inspect_server(script: str):
    params = StdioServerParameters(command="python", args=[script])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"  • {t.name}: {t.description[:60]}")

asyncio.run(inspect_server("mcp/servers/pricing_server.py"))
asyncio.run(inspect_server("mcp/servers/inventory_server.py"))
```

### SSE Mode (Multiple Clients)

```bash
# Terminal 1 — start servers
python mcp/servers/pricing_server.py --sse --port 8001
python mcp/servers/inventory_server.py --sse --port 8002

# Terminal 2 — connect to SSE server
python -c "
import asyncio
from mcp.client.sse import sse_client
from mcp import ClientSession
async def test():
    async with sse_client('http://localhost:8001/sse') as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            result = await s.call_tool('get_market_price', {'address': '742 Evergreen Terrace, Austin, TX 78701'})
            print(result.content[0].text[:200])
asyncio.run(test())
"
```

---

## Customization Guide

### Change the Property

Edit these values in `adk/negotiation_agents/buyer_agent/agent.py` and `seller_agent/agent.py`:

```python
PROPERTY_ADDRESS = "1234 Oak Street, Dallas, TX 75201"
LISTING_PRICE = 520_000
BUYER_BUDGET = 495_000
MINIMUM_PRICE = 475_000
```

Add the property to `mcp/servers/pricing_server.py`'s `PROPERTY_DATABASE`.

### Add a New MCP Tool

In `mcp/servers/pricing_server.py`:

```python
@mcp.tool()
def get_neighborhood_score(zip_code: str) -> dict:
    """Get neighborhood safety and amenity score."""
    return {
        "zip_code": zip_code,
        "safety_score": 8.2,
        "walkability": 7.5,
        "school_rating": 8.0,
    }
```

### Change Negotiation Strategy

In `adk/negotiation_agents/buyer_agent/agent.py`, modify the `instruction` string:

```python
# Change from "start 12% below asking" to "start 8% below"
# Or add: "Always ask for seller to cover closing costs"
```

### Add a Mediator Agent

Use ADK's workflow agents — wrap buyer, mediator, and seller as `sub_agents` of a `SequentialAgent` (or a custom routing agent) and orchestrate over A2A.

---

## Key Files Reference

| File | Key Element | What It Does |
|---|---|---|
| `mcp/servers/pricing_server.py` | `get_market_price`, `calculate_discount` | MCP pricing tools |
| `mcp/servers/inventory_server.py` | `get_inventory_level`, `get_minimum_acceptable_price` | MCP inventory tools |
| `adk/negotiation_agents/buyer_agent/agent.py` | `root_agent = LlmAgent(...)` | Buyer agent with McpToolset |
| `adk/negotiation_agents/seller_agent/agent.py` | `root_agent = LlmAgent(...)` | Seller agent with dual McpToolsets |
| `adk/negotiation_agents/negotiation/agent.py` | `root_agent = LoopAgent(...)` | LoopAgent + SequentialAgent + MCP tools + submit_decision |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'mcp'`**
```bash
pip install mcp
```

**`AuthenticationError` from OpenAI**
```bash
export OPENAI_API_KEY=sk-your-actual-key
```

**`AuthenticationError` / provider auth failure in ADK runs**
```bash
export OPENAI_API_KEY=sk-your-actual-key
```

**`FileNotFoundError` running MCP servers**
```bash
# Run from the mcp_a2a_gcp_practice/ directory
cd mcp_a2a_gcp_practice
python mcp/servers/pricing_server.py  # Not: python mcp_a2a_gcp_practice/mcp/servers/pricing_server.py
```

**GitHub MCP demo says `GITHUB_TOKEN not set (or is a placeholder)` or `401 Unauthorized`**
```bash
# .env still has the placeholder from .env.example, or the token is invalid/expired.
# Create a token: GitHub → Settings → Developer Settings → Personal Access Tokens
# (read access to public repositories is enough), then set GITHUB_TOKEN=... in .env
```

**PowerShell `UnauthorizedAccess` error activating venv**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\.venv\Scripts\Activate.ps1
```

**Unicode / encoding errors on Windows (`UnicodeEncodeError`, garbled output)**
```powershell
# Set UTF-8 mode before running any script
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
adk web adk/negotiation_agents/
```
Or add `PYTHONUTF8=1` to your `.env` file to make it permanent.

---

*Built for the AI Agent Systems Workshop — teaching MCP, A2A, and Google ADK through a real estate negotiation simulator.*
