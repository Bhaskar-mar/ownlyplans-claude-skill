# Resource categories

The MCP `kind` filter accepts exactly: `component`, `plan`, `skill`, `mcp`, `plugin`. A new kind may appear later. The tool's `kind` enum lists the current set. Read it instead of assuming.

## component (UI elements)
Self-contained interface pieces (buttons, cards, navigation, modals, charts and so on) with a live preview. Item data includes code (`html`, `css`, `js`, sometimes `react`) or an install command. Best for: landing pages, dashboards, design polish. Check: framework fit (plain HTML/CSS/JS vs React), dependencies, whether it assumes a dark or light background, and mobile behaviour.

## plan (development plans)
Ordered steps. Each step has an explanation, a prompt to paste, a "done when" check and the files it uses. Best for: building a whole feature or app, or giving a beginner a path. Walk steps in order with `get_step`. Do not skip the "done when" checks.

## skill (Claude skills)
A `SKILL.md` that changes how Claude handles a task. Install command writes it to `~/.claude/skills/<name>/SKILL.md`. Best for: repeatable workflows such as reviews or migrations. Read the file with `get_asset` before installing. A skill is instructions Claude will follow, so check it does what its summary says.

## mcp (MCP servers)
Listings with a config for connecting a tool to data or services. Check the transport (local command vs remote URL), required credentials, and what the server can read or change. Never ask the user to paste real secrets into chat.

## plugin (Claude Code plugins)
Plugin marketplaces to add to Claude Code. Check what the marketplace contains and the add command in the item.

## Mixing kinds
Most projects need a mix, for example a plan for the roadmap, components for the UI, an MCP server for data and a skill for review. Recommend each kind only when it earns its place.
