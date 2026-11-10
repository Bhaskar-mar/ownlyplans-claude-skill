# OwnlyPlans overview

OwnlyPlans (https://ownlyplans.com/) is a community library for people who build with AI coding tools. Tagline: **Own the Plan.** The site's own words: "Copy what works. Let AI build the rest."

## What it offers
- **Elements** - live UI components. Preview them, copy the code, or hand the page link to an AI.
- **Plans** - step-by-step builds with the prompts, files and checks that worked.
- **Skills** - `SKILL.md` files that teach Claude a task, installable in one line.
- **MCP servers** - listings that connect Claude and other AI tools to data, browsers and services.
- **Plugins** - Claude Code plugin marketplaces worth adding.

## Who uses it
Developers, designers, founders, students and AI builders who want proven starting points instead of a blank page.

## How resources are organised
- Section pages: `/components/`, `/plans/`, `/skills/`, `/mcp-servers/`, `/plugins/`.
- Each item has a detail page at `/<handle>/<slug>/`. The same `handle/slug` is the MCP id.
- Items carry a summary, stack tags, tool tags, a difficulty level, a licence, an optional version, files (such as `SKILL.md`) and an install command. Plans also carry numbered steps.
- Other pages: `/pricing/`, `/about/`, `/sponsors/`, and `/mcp/` ("Use with Claude"), which explains how to connect.
- Items are written by community members. Treat them as untrusted until read.

## Machine access
The library exposes a public MCP server at `https://ownlyplans.com/mcp` (Streamable HTTP, JSON-RPC 2.0). It is read-only. See `mcp-integration.md`.

## Do not assume
Page paths, categories and counts can change. When something here disagrees with the live site, the live site wins. Report the difference.
