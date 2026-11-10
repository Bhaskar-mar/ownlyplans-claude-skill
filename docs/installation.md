# Installation

Two separate things can be set up. You can do either or both:

1. **The skill** teaches Claude *how* to use OwnlyPlans (this repository).
2. **The MCP server** gives Claude *live access* to the library (`https://ownlyplans.com/mcp`).

The skill works best with the MCP server connected, but it has fallbacks if you skip it.

Sources for the install conventions: the official [Claude Code skills docs](https://code.claude.com/docs/en/skills).

## 1. Install the skill in Claude Code

### Personal (all your projects)
```bash
git clone https://github.com/Bhaskar-mar/ownlyplans-claude-skill.git ~/.claude/skills/ownlyplans
```

### One project only
```bash
git clone https://github.com/Bhaskar-mar/ownlyplans-claude-skill.git .claude/skills/ownlyplans
```

Replace `Bhaskar-mar` with the GitHub account that hosts the repository. The folder must contain `SKILL.md` at its top level.

### Manual install (no git)
1. Download the repository as a ZIP from GitHub and unzip it.
2. Rename the folder to `ownlyplans`.
3. Move it to `~/.claude/skills/` (personal) or `.claude/skills/` in your project.

### Verify it loaded
- Type `/` in Claude Code and look for `ownlyplans`, or run `/skills`.
- Or ask: "Find a UI element for a pricing table on OwnlyPlans" and watch for it to use the skill.
- Edits to an existing skill folder are picked up live. If you just created the top-level `skills` folder, run `/reload-skills` or restart.
- If it does not appear, start `claude --debug` and search the log for `[names]`.

### Update
```bash
git -C ~/.claude/skills/ownlyplans pull
```

### Uninstall
```bash
rm -rf ~/.claude/skills/ownlyplans
```

## 2. Install the skill in Claude.ai (optional)

Claude.ai accepts skills as a ZIP upload. Build one:
```bash
git clone https://github.com/Bhaskar-mar/ownlyplans-claude-skill.git ownlyplans
zip -r ownlyplans.zip ownlyplans -x "ownlyplans/.git/*" "ownlyplans/.github/*"
```
Then add it from Claude's settings, in the Skills section. The menu names change between releases, so check the current [Claude Help Center](https://support.claude.com) for the exact path. This repository's `SKILL.md` only uses frontmatter keys (`name`, `description`) that uploads accept.

Note: the helper script needs a shell with network access. In chat environments without it, the skill uses the MCP tools or website pages instead.

## 3. Connect the MCP server (separate from the skill)

Claude Code:
```bash
claude mcp add --transport http ownlyplanscom https://ownlyplans.com/mcp
```

Other MCP clients (JSON config):
```json
{ "mcpServers": { "ownlyplanscom": { "url": "https://ownlyplans.com/mcp" } } }
```

Verify: ask Claude "What tools does the ownlyplanscom MCP server provide?" You should see `search_items`, `get_item`, `get_step`, `get_asset` and `list_trending`. The server is read-only and needs no login.

The site's own page [Use with Claude](https://ownlyplans.com/mcp/) has the current instructions.

## Requirements
- Claude Code, or another Claude product that supports skills.
- Optional: Python 3.8+ for `scripts/ownlyplans_mcp.py`. No packages to install.
- Optional: network access to `ownlyplans.com`.
