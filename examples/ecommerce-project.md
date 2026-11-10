# Example: e-commerce project

> Illustrative. Shows how the skill mixes kinds and reports gaps honestly.

**User:** Help me build an e-commerce website for handmade candles. I'm a beginner.

**Claude:** asks one question: "Do you want to build with plain HTML, or a tool like WordPress?" The user picks WordPress.

Searches: `plan` for `ecommerce`, `shop`, `woocommerce`; `component` for `cards`, `cart`, `toast`; `plugin` for `shop`, `payments`; `mcp` for `payments`.

**Answer (shape):**
- **Best match, plan:** the closest verified plan from the search, with its steps summarised in plain language and the first step shown with its prompt. If no plan matches WordPress shops, Claude says so instead of picking a loose one.
- **UI pieces:** cards for products (for example *Selectable and Settings Cards*, https://ownlyplans.com/bhaskar/selectable-and-settings-cards/) and a toast for "added to cart" (*Animated Toast Stack*), each checked for WordPress fit.
- **Plugins / MCP:** only if verified items exist. Otherwise: "OwnlyPlans has no verified payments plugin yet. I can still explain how WooCommerce handles checkout, labelled as general advice."

Beginner style: one command per step, plain explanations, no jargon without a definition.

Closing line: "Verified: items fetched via MCP. Not done: nothing has been installed yet. Say 'go' and I will start with step 1."
