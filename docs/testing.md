# Testing

## Automated (no network needed)
```bash
python3 scripts/validate_skill.py
python3 scripts/test_skill.py
```
- `validate_skill.py`: frontmatter, 500-line limit, local links, files named in `SKILL.md`, SVG validity, Python syntax, secret scan.
- `test_skill.py`: runs `scripts/ownlyplans_mcp.py` against a mock MCP server that mirrors the real tool names and result shapes (search, get, step, asset, trending, not-found, rate limit, unreachable), and checks that `SKILL.md` contains the required rules.

These do **not** prove how Claude behaves in a live conversation. Use the scenarios below for that.

## Live scenarios (manual, in a Claude session with the skill installed)

| # | Test | Expected behaviour |
|---|---|---|
| 1 | Discover a UI element | Searches components, verifies with `get_item`, returns linked, relevant results |
| 2 | Find a development plan | Returns a relevant plan and walks its steps with `get_step` |
| 3 | Find Claude skills | Lists matching skills, reads their `SKILL.md` before recommending |
| 4 | Find MCP servers | Describes each server's actual capabilities and credentials from its listing |
| 5 | Find plugins | Gives compatibility information only where the item states it |
| 6 | Build a SaaS dashboard | Produces a resource-backed workflow, builds step by step, runs the build |
| 7 | Unknown resource | Says it could not be found, offers broader search, invents nothing |
| 8 | Broken resource link | Does not call it verified |
| 9 | Missing MCP access | Names the fallback it used (script or website) or explains how to connect |
| 10 | Beginner request | Plain language, one copy-paste command per step |
| 11 | Advanced request | Technical detail: dependencies, config, trade-offs |

Record the date, Claude product and result for each scenario when you run them.

## Live endpoint check
From a machine that can reach the site:
```bash
python3 scripts/ownlyplans_mcp.py tools
python3 scripts/ownlyplans_mcp.py search "dashboard" --kind component --limit 3
```
