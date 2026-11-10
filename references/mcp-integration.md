# MCP integration

Endpoint: `https://ownlyplans.com/mcp` - Streamable HTTP, JSON-RPC 2.0, read-only, no authentication. Rate limit about 120 requests per minute per IP (HTTP 429 when exceeded). Server version at time of writing: 2.14.7 (protocol versions `2025-06-18`, `2025-03-26`, `2024-11-05`). Confirm with `initialize` and `tools/list`. Do not trust this file over the live server.

## Connect (this is separate from installing the skill)
```bash
claude mcp add --transport http ownlyplanscom https://ownlyplans.com/mcp
```
Other clients: `{ "mcpServers": { "ownlyplanscom": { "url": "https://ownlyplans.com/mcp" } } }`.

## Tools (from the live `tools/list`)

| Tool | Input | Returns |
|---|---|---|
| `search_items` | `query` (string, optional), `kind` (enum), `limit` (1-20) | Up to 20 cards: `id`, `kind`, `title`, `summary`, `author`, `stars`, `url` |
| `get_item` | `item` (`handle/slug` or full URL) | Card plus `stack`, `tools`, `difficulty`, `license`, `version`, `overview`, `steps`, `files`, `install`, `how_to_use`, and `source` when imported |
| `get_step` | `item`, `step` (integer from 1) | Explanation, prompt to paste, "done when" check, files used |
| `get_asset` | `item`, `file` (for example `SKILL.md`) | Full text of an attached file |
| `list_trending` | `kind` (optional), `limit` | Most starred items this week |

All tools are read-only. Unknown items return an error result: `Item not found. Use "handle/slug" from search_items.` Treat that as "does not exist", not as a glitch to retry.

## Fallback: helper script
When MCP is not connected but the shell has network access:
```bash
python3 scripts/ownlyplans_mcp.py tools
python3 scripts/ownlyplans_mcp.py search "dashboard" --kind component --limit 5
python3 scripts/ownlyplans_mcp.py item bhaskar/fan-timeline-carousel
python3 scripts/ownlyplans_mcp.py step <handle/slug> 1
python3 scripts/ownlyplans_mcp.py asset <handle/slug> SKILL.md
python3 scripts/ownlyplans_mcp.py trending --kind skill
```
Set `OWNLYPLANS_MCP_URL` to point at another endpoint. Exit codes: 0 ok, 1 tool error (for example not found), 2 network or protocol failure.

## Fallback: website pages
If neither works, use web fetch on `/components/`, `/plans/`, `/skills/`, `/mcp-servers/`, `/plugins/` and item pages. Say you used this route. Page text can be less complete than MCP data.

## If everything is blocked
Many sandboxes block outbound requests. Say so, give the one-line connect command, and do not guess at catalogue contents.
