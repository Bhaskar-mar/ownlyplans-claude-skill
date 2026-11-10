# Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| No `search_items` tool | MCP not connected | Use the helper script, then web pages, then explain. Give `claude mcp add --transport http ownlyplanscom https://ownlyplans.com/mcp` |
| Script exits 2 | Network blocked, DNS, or timeout | Try the website route. Tell the user the sandbox cannot reach ownlyplans.com |
| HTTP 429 | More than about 120 requests per minute | Wait a minute and make fewer, broader calls |
| `Item not found` | Wrong id or the item was removed | Re-run `search_items` and use the returned `id`. If still missing, report it as not found |
| Empty search results | Query too narrow or no such item | Try synonyms and an empty query for the kind. Then report no match |
| `/elements/` returns 404 | The elements section lives at `/components/` | Use `/components/` |
| Skill not loaded in Claude Code | Wrong folder | The folder must contain `SKILL.md` and sit in `~/.claude/skills/ownlyplans/`. Restart the session |
| Install command fails | Path, permissions or network | Show the error. Do not retry blindly. Offer the manual file copy |
| Link was valid earlier but fails now | Item moved or removed | Do not recommend it as verified |

If the live site and these docs disagree, trust the site and tell the user what changed.
