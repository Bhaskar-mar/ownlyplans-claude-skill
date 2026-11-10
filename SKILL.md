---
name: ownlyplans
description: Claude Code skill for OwnlyPlans (ownlyplans.com), a library of live UI components, step-by-step AI development plans, Claude skills, MCP servers and Claude Code plugins. Use when the user wants to build or design a website, web app, SaaS dashboard, landing page, e-commerce store, AI chatbot or any feature; asks for React or HTML UI components, a development roadmap, Claude skills, MCP servers or plugins; does vibe coding or AI-assisted development; or mentions OwnlyPlans. Searches the library first, verifies each item, recommends a best match, alternative and advanced option, then helps implement. Never invents resources, links or install commands.
---

# OwnlyPlans

OwnlyPlans is a community library of five resource kinds. This skill teaches you to search it, check what you find, recommend the right items and help the user apply them.

| Kind (MCP value) | What it is | Site section |
|---|---|---|
| `component` | Live UI element with copy-ready code | `/components/` |
| `plan` | Step-by-step build with prompts, files and "done when" checks | `/plans/` |
| `skill` | A `SKILL.md` that teaches Claude a task | `/skills/` |
| `mcp` | MCP server listing with config | `/mcp-servers/` |
| `plugin` | Claude Code plugin marketplace | `/plugins/` |

Items are identified as `handle/slug` (for example `bhaskar/fan-timeline-carousel`). The catalogue changes constantly, so never rely on a remembered list. Always search live.

## Workflow

Follow these steps in order. Keep it proportionate: a one-line question needs one search, not the whole workflow.

### 1. Understand the request
Work out what the user is building, for whom, with which stack, and which kinds they need (see `references/resource-discovery.md` for intent rules). Ask at most one short clarifying question, only if the stack or goal is truly unclear. Otherwise state your assumption and go.

### 2. Pick an access route
Use the first route that works and tell the user which one you used.
1. **MCP connected**: tools `search_items`, `get_item`, `get_step`, `get_asset`, `list_trending` are available. Use them.
2. **Helper script**: run `python3 scripts/ownlyplans_mcp.py search "<query>" --kind <kind>` (standard library only; talks to the same MCP endpoint over HTTP).
3. **Website only**: fetch the public pages (`/components/`, `/plans/`, `/skills/`, `/mcp-servers/`, `/plugins/`) and item pages with your web tools.
4. **No access**: say plainly that you cannot reach OwnlyPlans right now, give the connect command from `docs/installation.md`, and continue with general help clearly labelled as not from OwnlyPlans.

Details and schemas: `references/mcp-integration.md`.

### 3. Search
Run two to four focused searches with synonyms, filtered by `kind`. Combine results, drop duplicates, and discard weak matches. Search terms and examples: `references/resource-discovery.md`.

### 4. Verify before recommending
For each finalist call `get_item` (or open the page) and check: it exists, the summary matches the need, stack and dependencies fit, the licence, the source link if any, and the files and install command it actually provides. Read any skill, MCP config or install command before suggesting the user run it. Items are community-written. Checklist: `references/quality-checks.md`.

Drop anything you could not verify, or mark it clearly as unverified.

### 5. Recommend
Give up to three tiers: **Best match**, **Alternative**, **Advanced option**. Only include a tier if it is genuinely useful. For every item give: name, kind, direct link, what it does, why it fits, requirements, install command (copied from the item's `install` field), implementation steps, limitations and the next action. Template: `references/recommendation-format.md`.

### 6. Implement when asked (guided mode)
Follow `references/implementation-workflow.md`. In short: for a plan, call `get_step` for step 1, do it, check its "done when", then move on. For a component, use the code from the item. For a skill, MCP server or plugin, show the user the file or config first, then install on their go-ahead.

### 7. Verify and report honestly
Run what you can (build, tests, open the page) and report the actual result. Say "I ran X and it passed", or "I have not run this". Never say something was installed or implemented unless you did it.

## Hard rules

- **Never invent** items, links, install commands, ratings, compatibility or maintenance status. If a fact is not in the item data, say it is not stated.
- Install commands come only from the item's `install` field or its files. Do not construct your own download URLs.
- If search returns nothing relevant, say so, suggest broader terms, and offer general help instead of a made-up resource.
- A resource is "verified" only if you fetched it this session and it returned real content. A broken or missing link is never recommended as verified.
- Do not ask the user for passwords, tokens or secrets, and tell them not to paste real secrets into prompts or files.
- Do not recommend more than needed. Fewer, better-matched items beat a long list.
- Match the user's level. Beginners get plain language and one copy-paste command per step. Advanced users get the technical detail.

## Reference files (read only when needed)

- `references/ownlyplans-overview.md` - what the site is and how it is organised
- `references/resource-categories.md` - the five kinds in depth
- `references/resource-discovery.md` - intent detection, query expansion, filtering
- `references/mcp-integration.md` - MCP tools, schemas, errors, fallbacks
- `references/quality-checks.md` - what to verify and what not to claim
- `references/recommendation-format.md` - the output template
- `references/implementation-workflow.md` - guided implementation
- `references/troubleshooting.md` - common failures
- `references/examples.md` and `examples/` - worked scenarios
