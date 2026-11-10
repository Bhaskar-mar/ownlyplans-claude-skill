# Example: AI chatbot (including an unknown-resource case)

> Illustrative.

**User:** Find the best resources for building an AI chatbot, advanced level. Is there an OwnlyPlans plan called "Chatbot Pro Kit"?

**Claude:**
1. `search_items` with `query="Chatbot Pro Kit"` returns no match. `get_item` for a guessed id returns `Item not found`.
2. Reports: "I could not find an item called Chatbot Pro Kit on OwnlyPlans."
3. Broadens: searches `chatbot`, `assistant`, `rag`, `llm`, `mcp` across plans, skills and MCP servers.
4. Recommends only what verifies. For example an MCP server that reads documents (*MarkItDown MCP Server*, https://ownlyplans.com/bhaskar/markitdown-mcp-server/) as an ingestion step, after reading its config and stating what it can access.
5. Says clearly where OwnlyPlans has nothing and offers general architecture advice, labelled as not from OwnlyPlans.

Advanced detail: transport and credentials for the MCP server, where retrieval fits, evaluation and prompt-injection risks when ingesting untrusted documents.
