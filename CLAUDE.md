# CLAUDE.md

## Project: openai-agents-python

**Organization:** AiFeatures (iAiFy Enterprise)
**Language:** Python
**Description:** Lightweight framework for building multi-agent workflows, provider-agnostic with support for 100+ LLMs

## Build & Test

```bash
# Install dependencies
uv sync --all-extras --all-packages --group dev

# Run all tests
make tests

# Run tests in parallel (default)
uv run pytest -n auto --dist loadfile -m "not serial"

# Run serial tests only
uv run pytest -m serial

# Lint
make lint
# or: uv run ruff check

# Format
make format
# or: uv run ruff format

# Type checking
make typecheck
# runs mypy + pyright in parallel

# Coverage
make coverage

# Full pre-PR check (format + lint + typecheck + tests)
make check

# Build docs
make build-docs

# Serve docs locally
make serve-docs
```

## Architecture

```text
src/agents/            # Core SDK package
  agent.py             # Agent class with instructions, tools, guardrails, handoffs
  runner.py            # Runner for executing agent workflows
  tools/               # Tool implementations (functions, MCP, hosted)
  guardrails/          # Input/output validation
  tracing/             # Built-in run tracking and debugging
  sessions/            # Conversation history management
  realtime/            # Voice agent support
tests/                 # Test suite
examples/              # Usage examples and demos
docs/                  # MkDocs documentation source
```

## Conventions

- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`
- Kebab-case file names
- Branch protection on main -- PRs required
- Python >= 3.10 required
- Ruff for linting and formatting (line-length 100)
- mypy + pyright for type checking
- pytest with asyncio auto mode

## Shared Resources

| Asset | Location |
| --- | --- |
| CI/CD workflows | Ai-road-4-You/enterprise-ci-cd@v1 |
| Composite actions | Ai-road-4-You/github-actions@v1 |
| Governance | Ai-road-4-You/governance |

## Fork Info

- Upstream: openai/openai-agents-python
- Do NOT create PRs to upstream
- Sync managed by Ai-road-4-You/fork-sync
- iAiFy-originated changes are MIT unless upstream license requires otherwise
