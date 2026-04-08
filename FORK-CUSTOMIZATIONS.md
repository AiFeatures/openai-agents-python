# Fork Customizations

> Upstream: [openai/openai-agents-python](https://github.com/openai/openai-agents-python)
> Fork maintained by: @ashsolei
> Last reviewed: 2026-04-08
> Fork type: **active-dev**
> Sync cadence: **monthly**

## Purpose of Fork

OpenAI Agents SDK; iAiFy tracks upstream closely and layers enterprise governance.

## Upstream Source

| Property | Value |
|---|---|
| Upstream | [openai/openai-agents-python](https://github.com/openai/openai-agents-python) |
| Fork org | AiFeatures |
| Fork type | active-dev |
| Sync cadence | monthly |
| Owner | @ashsolei |

## Carried Patches

Local commits ahead of `upstream/main` at last review:

- `cb03cce0 chore(deps): bump pyjwt from 2.10.1 to 2.12.0 (#1)`
- `8776cf99 chore(deps): bump protobuf from 5.29.5 to 5.29.6 (#2)`
- `05065bd1 chore(deps): bump filelock from 3.18.0 to 3.20.3 (#4)`
- `3fedb1cf chore(deps): bump python-multipart from 0.0.20 to 0.0.22 (#5)`
- `974d0826 chore(deps): bump urllib3 from 2.5.0 to 2.6.3 (#7)`
- `3cb55ebf chore(deps): bump requests from 2.32.4 to 2.33.0 (#8)`
- `b31edd18 chore(deps-dev): bump cryptography from 45.0.7 to 46.0.6 (#9)`
- `85bf3706 chore(deps): bump pygments from 2.19.2 to 2.20.0 (#10)`
- `b4c6d38b chore(deps): bump aiohttp from 3.12.15 to 3.13.4 (#11)`
- `42e8e1b8 chore(deps): bump litellm from 1.81.0 to 1.83.0 (#12)`
- `815ed487 chore: remove obsolete .agents/skills definitions`
- `50f1fe1d docs: update FORK-CUSTOMIZATIONS.md with upstream source`
- `211f1c8c docs: add FORK-CUSTOMIZATIONS.md per enterprise fork governance`
- `1eb6f92e ci: add copilot-setup-steps.yml for Copilot Workspace`
- `1b938a67 chore: add copilot-instructions.md`
- `2082f728 chore: add Copilot Coding Agent setup steps`
- `02f50e6e chore: remove misplaced agent files from .github/copilot/agents/`
- `fde75b43 chore: deploy core custom agents from AgentHub`
- `36786ecc chore: deploy core Copilot agents from AgentHub`
- `3ee70bd3 docs: add FORK-CUSTOMIZATIONS.md`
- `eedccbc2 chore: add CODEOWNERS [governance-orchestrator]`
- `67cb84e8 chore: remove workflow update-docs.yml — enterprise cleanup`
- `879a80a8 chore: remove workflow tests.yml — enterprise cleanup`
- `fe3667f4 chore: remove workflow release-tag.yml — enterprise cleanup`
- `99689b9d chore: remove workflow release-pr.yml — enterprise cleanup`
- ... (5 more commits ahead of `upstream/main`)

## Supported Components

- Root governance files (`.github/`, `CLAUDE.md`, `AGENTS.md`, `FORK-CUSTOMIZATIONS.md`)
- Enterprise CI/CD workflows imported from `Ai-road-4-You/enterprise-ci-cd`

## Out of Support

- All upstream source directories are tracked as upstream-of-record; local edits to core source are discouraged.

## Breaking-Change Policy

1. On upstream sync, classify per `governance/docs/fork-governance.md`.
2. Breaking API/license/security changes auto-classify as `manual-review-required`.
3. Owner triages within 5 business days; conflicts are logged to the `fork-sync-failure` issue label.
4. Revert local customizations only after stakeholder sign-off.

## Sync Strategy

This fork follows the [Fork Governance Policy](https://github.com/Ai-road-4-You/governance/blob/main/docs/fork-governance.md)
and the [Fork Upstream Merge Runbook](https://github.com/Ai-road-4-You/governance/blob/main/docs/runbooks/fork-upstream-merge.md).

- **Sync frequency**: monthly
- **Conflict resolution**: Prefer upstream; reapply iAiFy customizations on a sync branch
- **Automation**: [`Ai-road-4-You/fork-sync`](https://github.com/Ai-road-4-You/fork-sync) workflows
- **Failure handling**: Sync failures create issues tagged `fork-sync-failure`

## Decision: Continue, Rebase, Refresh, or Replace

| Option | Current Assessment |
|---|---|
| Continue maintaining fork | yes - active iAiFy product scope |
| Full rebase onto upstream | feasible on request |
| Fresh fork (discard local changes) | not acceptable without owner review |
| Replace with upstream directly | not possible (local product value) |

## Maintenance

- **Owner**: @ashsolei
- **Last reviewed**: 2026-04-08
- **Reference runbook**: `ai-road-4-you/governance/docs/runbooks/fork-upstream-merge.md`
