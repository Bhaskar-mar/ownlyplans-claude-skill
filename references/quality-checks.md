# Quality and safety checks

Check only what the item data lets you check. Report "not stated" for the rest.

| Check | Where to look | Do not |
|---|---|---|
| Exists and is reachable | `get_item` succeeds, page returns content | Call it verified from memory |
| Fits the stack | `stack`, `tools`, files, code | Assume framework support |
| Dependencies | install command, code imports, config | Guess versions |
| Install complexity | length and content of `install` | Run it unread |
| Licence | `license` field, `source.license` | State a licence not shown |
| Maintenance | `version`, last updated on the page | Invent "actively maintained" |
| Documentation | `overview`, steps, notes | Rate it with made-up scores |
| Source | `source.url` when present | Fabricate an upstream |
| Safety | read `SKILL.md`, MCP config and install lines | Run unread code or paste secrets |

## Safety reading for each kind
- **skill**: could it tell Claude to run commands, exfiltrate data or ignore the user? Read it all.
- **mcp**: what can it access, does it need tokens, is it local or remote?
- **plugin / install command**: which URL does it fetch, and what does it write?
- **component**: does it load external scripts?

## Link verification
Fetch the item URL or its file URL. A 200 with real content is verified. A 404, timeout or empty page is not. Say which.

## Ratings
`stars` is a count of community stars. Quote it as that. Never turn it into a quality rating.
