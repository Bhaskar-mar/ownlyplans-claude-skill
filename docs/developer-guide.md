# Developer guide

## Layout
```
SKILL.md              entry point (frontmatter + workflow, under 500 lines)
references/           detail Claude loads on demand
examples/             worked conversations
scripts/              helper client, validator, tests
assets/               SVG banner, logo and diagrams
docs/                 human documentation
```

## Design rules
- **Progressive disclosure**: `SKILL.md` stays short and points at `references/`.
- **Dynamic**: no hardcoded catalogue. Search the live library.
- **Honest**: no invented resources, links, ratings or compatibility.
- **Skill and MCP are separate**: the skill is instructions, the MCP server is live data.

## Local checks
```bash
python3 scripts/validate_skill.py
python3 scripts/test_skill.py
python3 scripts/validate_skill.py --check-external   # also tests http(s) links, needs network
```
CI runs the first two on every push and pull request.

## MCP dependency
The skill targets the OwnlyPlans MCP server (tools `search_items`, `get_item`, `get_step`, `get_asset`, `list_trending`; protocol `2025-06-18` and two older versions). If the server changes a tool name or schema, update `references/mcp-integration.md`, `scripts/ownlyplans_mcp.py` and the mock server in `scripts/test_skill.py` together. New resource kinds appear in the `kind` enum. Add a line to `references/resource-categories.md`.

## Releasing
1. Update `CHANGELOG.md`.
2. Run both checks.
3. Commit, then `git tag -a vX.Y.Z -m "OwnlyPlans skill vX.Y.Z"` and `git push --tags`.
4. Create a GitHub release from the tag. Optionally attach `ownlyplans.zip` (see `docs/installation.md`).

Versioning: patch for wording fixes, minor for new behaviour or references, major for breaking changes to the workflow or script CLI.

## Extending the ecosystem
- A contribution workflow already exists on the site: members submit elements, plans, skills, MCP servers and plugins at https://ownlyplans.com/submit-a-plan/. Point contributors there for new resources. This repository only holds the skill.
