# CLAUDE.md — openai-agents-python (AiFeatures fork)

Upstream: openai/openai-agents-python — lightweight, provider-agnostic multi-agent workflow framework (Python 3.10+). Used within iAiFy to build and test agent orchestration patterns against the OpenAI Responses/Chat Completions API and 100+ other LLMs.

See AGENTS.md for the upstream agent instruction surface.

## Quick Start

```bash
# Python 3.10+ required
python -m venv .venv && source .venv/bin/activate

# Install
pip install openai-agents
# or with uv:
uv init && uv add openai-agents

# With optional extras
pip install 'openai-agents[voice]'    # voice support
pip install 'openai-agents[redis]'    # Redis session backend

# Run an example
python examples/basic/hello_world.py
```

## Development

```bash
pip install -e ".[dev]"
pytest               # run tests
mypy src/            # type check
ruff check .         # lint
ruff format .        # format
```

## Architecture

- `src/agents/` — Core SDK: Agent, Runner, Tools, Guardrails, Handoffs, Sessions, Tracing, Realtime
- `examples/` — Reference implementations organized by feature area
- `tests/` — Unit and integration tests
- `docs/` — MkDocs documentation source

Key concepts: **Agent** (instructions + tools + guardrails), **Runner** (sync/async execution), **Handoffs** (agent-to-agent delegation), **Sessions** (conversation history), **Tracing** (run visibility + debugging).

## Conventions

- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Kebab-case file names, snake_case Python identifiers
- Follow upstream openai/openai-agents-python release cadence for sync PRs

## Shared Resources

| Resource | Location |
| --- | --- |
| Reusable CI workflows | `Ai-road-4-You/enterprise-ci-cd` |
| AgentHub | `~/AgentHub/` (central hub, 12 MCP servers) |

## AgentHub

- Central hub: `~/AgentHub/`
- Skills: `.agents/skills/` (symlinked to AgentHub shared skills)
- MCP: 12 servers synced across all agents
- Agents: 14 shared agents available
- Hooks: Safety, notification, and logging hooks
