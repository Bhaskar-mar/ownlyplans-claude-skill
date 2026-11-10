# Contributing

Thanks for helping. This repository holds the Claude skill. To add resources to the OwnlyPlans library itself, use https://ownlyplans.com/submit-a-plan/.

## Good contributions
- Clearer or shorter instructions in `SKILL.md` and `references/`
- New or fixed example conversations
- Fixes for the helper script when the MCP server changes
- Better tests

## Rules
- Keep `SKILL.md` under 500 lines. Put detail in `references/`.
- Never hardcode catalogue contents. The library changes.
- Never add invented resources, links, install commands or ratings. Examples must use items you have verified, and say they are illustrative.
- No secrets, tokens or `.env` files.
- Standard library only for scripts.

## Before opening a pull request
```bash
python3 scripts/validate_skill.py
python3 scripts/test_skill.py
```
Describe what changed and why. If behaviour changed, note which scenario in `docs/testing.md` it affects.

## Reporting problems
Use the issue templates. For security issues see `SECURITY.md`.
