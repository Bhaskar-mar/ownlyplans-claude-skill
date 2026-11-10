# FAQ

**What is the difference between the skill and the MCP server?**
The skill teaches Claude how to use OwnlyPlans. The MCP server gives live read access to the library. They work best together, but each works alone with fallbacks.

**Do I need an account or API key?**
No. The MCP server is public and read-only.

**Why does Claude say it could not reach OwnlyPlans?**
Your environment may block outbound network access. Connect the MCP server from your own machine or let Claude use the website pages. See `references/troubleshooting.md`.

**Will it recommend things that do not exist?**
It is instructed never to. Every recommendation comes from a search result or item page it fetched. If nothing matches, it says so.

**Are OwnlyPlans resources safe to run?**
They are community-written. The skill tells Claude to read skills, MCP configs and install commands before suggesting you run them. You should read them too.

**Does it work offline?**
No. It needs access to the library.

**The site says `/elements/` is missing.**
The Elements section lives at `/components/`.

**How do I add my own resource to OwnlyPlans?**
Use the submit page on the site: https://ownlyplans.com/submit-a-plan/.

**How do I report a bug or a wrong recommendation?**
Open an issue using the templates in this repository.
