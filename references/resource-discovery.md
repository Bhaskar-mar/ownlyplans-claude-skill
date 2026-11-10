# Resource discovery

## Intent detection

| The user says... | Primary kind | Also consider |
|---|---|---|
| "dashboard", "landing page", "navbar", "modal", "table", "form", "animation" | component | plan |
| "roadmap", "step by step", "build me a ...", "from scratch", "startup idea" | plan | component, mcp |
| "Claude skill", "improve my workflow", "review code", "SKILL.md" | skill | plugin |
| "MCP", "connect to database / browser / GitHub / Slack" | mcp | skill |
| "plugin", "marketplace", "Claude Code extension" | plugin | skill |
| "help me build X" (broad) | plan | component, skill, mcp, plugin |

If the request is mixed, search several kinds, then keep only what the project needs.

## Query expansion
Search several short queries rather than one long sentence. Use the user's words plus synonyms and the parts a feature needs.

Example: "CRM dashboard" - search `dashboard`, `admin`, `analytics`, `data table`, `chart`, `auth`, `forms`, `user management`, each with the right `kind`.

Tips:
- Short nouns beat sentences. `supabase booking` works better than "something to take bookings".
- An empty query lists the newest items. Use it to see what exists in a kind.
- Stack and tool tags are searched as well as text, so include the framework (`react`, `wordpress`) when it matters.
- `list_trending` shows the most starred items this week. It is a popularity hint, not a quality guarantee.

## Filtering
1. Remove duplicates by `id`.
2. Drop items whose summary does not match the need.
3. Drop items that do not fit the stack.
4. Rank by fit first, then simplicity, then stars.
5. Keep at most three tiers (best, alternative, advanced).

## When nothing matches
Say "OwnlyPlans has no verified match for X". Offer broader search terms, and optionally general help labelled as not from OwnlyPlans. Never fill the gap with an invented item.
