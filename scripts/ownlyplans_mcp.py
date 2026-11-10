#!/usr/bin/env python3
"""Tiny OwnlyPlans MCP client (standard library only).

Talks to the public, read-only MCP endpoint over HTTP JSON-RPC so the skill
still works where an MCP client is not configured.

Exit codes: 0 ok, 1 tool returned an error (e.g. item not found),
            2 network or protocol failure.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = "https://ownlyplans.com/mcp"
PROTOCOL = "2025-06-18"
TIMEOUT = 20


class McpError(Exception):
    """Network or protocol failure (exit code 2)."""


def rpc(url, method, params=None, req_id=1, timeout=TIMEOUT):
    body = json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "ownlyplans-claude-skill/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            raise McpError("Rate limited (HTTP 429). Wait a minute and retry with fewer calls.")
        raise McpError("HTTP %s from %s" % (exc.code, url))
    except (urllib.error.URLError, OSError) as exc:
        raise McpError("Cannot reach %s: %s" % (url, exc))
    try:
        data = json.loads(raw)
    except ValueError:
        raise McpError("Response was not JSON")
    if "error" in data:
        raise McpError("Protocol error: %s" % data["error"].get("message", data["error"]))
    return data.get("result", {})


def call_tool(url, name, arguments):
    rpc(url, "initialize", {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": {"name": "ownlyplans-claude-skill", "version": "1.0.0"}})
    result = rpc(url, "tools/call", {"name": name, "arguments": arguments}, req_id=2)
    text = "".join(c.get("text", "") for c in result.get("content", []) if c.get("type") == "text")
    return bool(result.get("isError")), text


def build_parser():
    p = argparse.ArgumentParser(description="Query the OwnlyPlans MCP server.")
    p.add_argument("--url", default=os.environ.get("OWNLYPLANS_MCP_URL", DEFAULT_URL))
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("tools", help="list the tools the server offers")
    s = sub.add_parser("search", help="search items")
    s.add_argument("query", nargs="?", default="")
    s.add_argument("--kind")
    s.add_argument("--limit", type=int, default=10)
    i = sub.add_parser("item", help="get one item")
    i.add_argument("item")
    st = sub.add_parser("step", help="get one plan step")
    st.add_argument("item")
    st.add_argument("step", type=int)
    a = sub.add_parser("asset", help="read a file attached to an item")
    a.add_argument("item")
    a.add_argument("file")
    t = sub.add_parser("trending", help="most starred this week")
    t.add_argument("--kind")
    t.add_argument("--limit", type=int, default=10)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "tools":
            rpc(args.url, "initialize", {"protocolVersion": PROTOCOL, "capabilities": {}, "clientInfo": {"name": "ownlyplans-claude-skill", "version": "1.0.0"}})
            print(json.dumps(rpc(args.url, "tools/list", req_id=2).get("tools", []), indent=2))
            return 0
        if args.cmd == "search":
            name, payload = "search_items", {"query": args.query, "limit": args.limit}
            if args.kind:
                payload["kind"] = args.kind
        elif args.cmd == "item":
            name, payload = "get_item", {"item": args.item}
        elif args.cmd == "step":
            name, payload = "get_step", {"item": args.item, "step": args.step}
        elif args.cmd == "asset":
            name, payload = "get_asset", {"item": args.item, "file": args.file}
        else:
            name, payload = "list_trending", {"limit": args.limit}
            if args.kind:
                payload["kind"] = args.kind
        is_error, text = call_tool(args.url, name, payload)
    except McpError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    print(text)
    return 1 if is_error else 0


if __name__ == "__main__":
    sys.exit(main())
