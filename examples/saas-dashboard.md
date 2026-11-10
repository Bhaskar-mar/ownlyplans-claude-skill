# Example: SaaS dashboard

> Illustrative transcript. Item ids below existed on ownlyplans.com when this was written. Real results depend on the live catalogue, so Claude always searches again.

**User:** Find the best UI elements for a modern SaaS dashboard. I'm using plain HTML/CSS/JS.

**Claude (what it does):** searches `kind=component` for `sidebar`, `data table`, `status`, `pagination`; calls `get_item` on the finalists; checks each is plain HTML/CSS/JS.

**Claude (answer):**

### Best match: Collapsible Icon Rail Sidebar (component)
Link: https://ownlyplans.com/bhaskar/collapsible-icon-rail-sidebar/
What it does: app sidebar with workspace switcher and nav items that folds to an icon rail.
Why it fits: gives your dashboard its shell, and is plain HTML/CSS/JS as required.
Requirements: none beyond a browser (no dependencies in the item).
Install: copy the HTML, CSS and JS from the item page.
Steps: 1) paste the markup into your layout 2) merge the CSS 3) add the script before `</body>` 4) rename the nav labels.
Limits: demo content is placeholder. Routing is yours to wire.
Next: place it, then add the table.

### Alternative: Sortable Data Table (component)
Link: https://ownlyplans.com/bhaskar/sortable-data-table-2/
Why it fits: sortable columns, row selection and status badges for lists of customers or invoices.
Limits: data is generated in the script. Replace it with your API data.

### Advanced option
Pair the two with a plan item from `/plans/` if one matches your backend. None was a verified match for "auth and billing" in this search, so none is recommended.

Verified: fetched all items through MCP. Not verified: how they look inside your app.

**User:** Great. Build it.

**Claude:** confirms the file layout, builds the shell first, then the table, runs the page, checks it at phone width and reports what it saw.
