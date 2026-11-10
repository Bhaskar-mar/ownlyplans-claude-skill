#!/usr/bin/env python3
"""Tests for the OwnlyPlans skill package. Standard library only.

Run: python3 scripts/test_skill.py

Part 1 exercises scripts/ownlyplans_mcp.py against a local mock MCP server
that follows the real server's tool names and result shapes.
Part 2 checks that SKILL.md encodes the behaviour in docs/testing.md.
These tests do not evaluate Claude's live behaviour; see docs/testing.md
for the manual scenario checklist.
"""
import io
import json
import re
import sys
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import ownlyplans_mcp as cli  # noqa: E402

ITEMS = {
    "bhaskar/demo-card": {"id": "bhaskar/demo-card", "kind": "component", "title": "Demo Card", "summary": "A card.", "url": "https://example.test/bhaskar/demo-card/", "stack": ["HTML"], "license": "cc-by-4.0", "install": "", "files": []},
    "bhaskar/demo-plan": {"id": "bhaskar/demo-plan", "kind": "plan", "title": "Demo Plan", "summary": "A plan.", "url": "https://example.test/bhaskar/demo-plan/", "steps": [{"title": "One"}]},
    "bhaskar/demo-skill": {"id": "bhaskar/demo-skill", "kind": "skill", "title": "Demo Skill", "summary": "A skill.", "url": "https://example.test/bhaskar/demo-skill/", "install": "mkdir -p ~/.claude/skills/demo-skill"},
}
TOOLS = ["search_items", "get_item", "get_step", "get_asset", "list_trending"]
STATE = {"rate_limit": False}


def ok(text):
    return {"content": [{"type": "text", "text": text}]}


def err(text):
    return {"isError": True, "content": [{"type": "text", "text": text}]}


class Mock(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        if STATE["rate_limit"]:
            self.send_response(429)
            self.end_headers()
            return
        msg = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        m, p = msg["method"], msg.get("params", {})
        if m == "initialize":
            res = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "mock"}}
        elif m == "tools/list":
            res = {"tools": [{"name": n} for n in TOOLS]}
        elif m == "tools/call":
            res = self.tool(p["name"], p["arguments"])
        else:
            body = json.dumps({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "nope"}}).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": res}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def tool(self, name, a):
        if name == "search_items":
            q, kind = a.get("query", "").lower(), a.get("kind")
            hits = [i for i in ITEMS.values() if (not kind or i["kind"] == kind) and (q in i["title"].lower() or q in i["summary"].lower())]
            return ok(json.dumps(hits))
        if name == "get_item":
            return ok(json.dumps(ITEMS[a["item"]])) if a["item"] in ITEMS else err('Item not found. Use "handle/slug" from search_items.')
        if name == "get_step":
            it = ITEMS.get(a["item"])
            if not it or a["step"] > len(it.get("steps", [])):
                return err("Step out of range.")
            return ok(json.dumps(it["steps"][a["step"] - 1]))
        if name == "get_asset":
            return ok("# SKILL") if a["item"] == "bhaskar/demo-skill" else err("File not found.")
        if name == "list_trending":
            return ok(json.dumps(list(ITEMS.values())[: a.get("limit", 10)]))
        return err("unknown tool")


def run(argv):
    out, errb = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(errb):
        code = cli.main(argv)
    return code, out.getvalue(), errb.getvalue()


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = HTTPServer(("127.0.0.1", 0), Mock)
        cls.url = "http://127.0.0.1:%d/mcp" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def setUp(self):
        STATE["rate_limit"] = False

    def cmd(self, *a):
        return run(["--url", self.url, *a])

    def test_tools_lists_real_tool_names(self):
        code, out, _ = self.cmd("tools")
        self.assertEqual(code, 0)
        self.assertEqual([t["name"] for t in json.loads(out)], TOOLS)

    def test_discover_ui_element(self):
        code, out, _ = self.cmd("search", "card", "--kind", "component")
        self.assertEqual(code, 0)
        self.assertEqual([h["id"] for h in json.loads(out)], ["bhaskar/demo-card"])

    def test_find_development_plan_and_step(self):
        self.assertEqual(self.cmd("search", "plan", "--kind", "plan")[0], 0)
        code, out, _ = self.cmd("step", "bhaskar/demo-plan", "1")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["title"], "One")

    def test_find_skills_and_read_file(self):
        self.assertEqual(json.loads(self.cmd("search", "skill", "--kind", "skill")[1])[0]["kind"], "skill")
        self.assertIn("SKILL", self.cmd("asset", "bhaskar/demo-skill", "SKILL.md")[1])

    def test_trending(self):
        self.assertEqual(self.cmd("trending", "--limit", "2")[0], 0)

    def test_unknown_resource_reports_not_found(self):
        code, out, _ = self.cmd("item", "bhaskar/missing")
        self.assertEqual(code, 1)
        self.assertIn("not found", out.lower())

    def test_empty_search_is_not_an_error(self):
        code, out, _ = self.cmd("search", "zzzz")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), [])

    def test_step_out_of_range_is_tool_error(self):
        self.assertEqual(self.cmd("step", "bhaskar/demo-plan", "9")[0], 1)

    def test_rate_limit_exit_2(self):
        STATE["rate_limit"] = True
        code, _, e = self.cmd("search", "x")
        self.assertEqual(code, 2)
        self.assertIn("429", e)

    def test_missing_mcp_access_is_clear_failure(self):
        code, _, e = run(["--url", "http://127.0.0.1:9/mcp", "search", "x"])
        self.assertEqual(code, 2)
        self.assertIn("Cannot reach", e)


class SkillContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.low = cls.skill.lower()

    def test_frontmatter(self):
        m = re.match(r"---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", self.skill)
        self.assertIsNotNone(m)
        self.assertLessEqual(len(m.group(2)), 1024)

    def test_covers_all_five_kinds(self):
        for kind in ("component", "plan", "skill", "mcp", "plugin"):
            self.assertIn("`%s`" % kind, self.skill)

    def test_uses_only_real_tools(self):
        for tool in re.findall(r"`((?:search|get|list)_[a-z_]+)`", self.skill):
            self.assertIn(tool, TOOLS)

    def test_no_hallucination_rules_present(self):
        self.assertIn("never invent", self.low)
        self.assertIn("not stated", self.low)
        self.assertIn("verified", self.low)

    def test_fallbacks_documented(self):
        self.assertIn("helper script", self.low)
        self.assertIn("no access", self.low)

    def test_beginner_and_advanced_levels(self):
        self.assertIn("beginners", self.low)
        self.assertIn("advanced", self.low)

    def test_honest_installation_claims(self):
        self.assertIn("never say something was installed", self.low)

    def test_scenarios_doc_lists_eleven(self):
        text = (ROOT / "docs" / "testing.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(re.findall(r"^\| \d+ \|", text, re.M)), 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
