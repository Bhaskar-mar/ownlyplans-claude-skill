# Guided implementation

Use when the user wants help building, not just a list.

## Flow
1. **Frame**: restate the goal, users, stack and constraints in two or three lines.
2. **Plan**: choose a plan item if one fits, otherwise outline your own steps and label them as yours.
3. **Gather**: collect only the components, skill, MCP server or plugin the plan needs.
4. **Confirm**: show the user the install commands and config you intend to use. Wait for a yes before running installs that change their machine or accounts.
5. **Build step by step**:
   - Plan item: `get_step` 1, do it, check "done when", report the result, then `get_step` 2, and so on.
   - Component: read the code from `get_item`, adapt names and styles to the project, keep the licence note if the item has one.
   - Skill: `get_asset` the `SKILL.md`, show it, then run the item's install command.
   - MCP server: show the config, explain access, add it, then test one call.
6. **Verify**: run the project's build, tests or a page check. Report real output.
7. **Review**: suggest improvements (accessibility, responsiveness, performance, security) and the next step.

## Honesty rules
- Say what you did and what you did not. "Installed" means the command ran and exited successfully.
- If a step fails, show the error and fix it or ask. Do not skip it silently.
- If an item's own claims could not be reproduced, say so.

## Worked outline: SaaS dashboard
1. Search `dashboard`, `data table`, `chart`, `sidebar`, `auth` as components. Search `dashboard` and `saas` as plans.
2. Pick one plan for the build order and a few components for the shell, table and charts.
3. Check stack fit, then build layout first, data next, polish last.
4. Run the build. Review responsiveness and accessibility.
