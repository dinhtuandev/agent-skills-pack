---
name: wire-mcp-server
description: Set up an MCP (Model Context Protocol) server connection for an external service or API inside a project. Use when the user wants to wire up, connect, or scaffold an MCP server, add MCP tools for a service, or integrate an external API into Claude Code via MCP.
---

# Wire Up an MCP Server

## Inputs

- **Service/API** being connected
- **Jobs to be done** — what the user actually needs it to do, concretely

## Steps

1. **Check for an existing server first.** Look for an official or well-maintained MCP server for this service before building one — name the source you found (or checked and didn't find).
2. **If one exists**: give the exact install command and a `.mcp.json` config scoped to this project — not a global install unless asked. `assets/mcp-config-template.json` has the shape to start from; verify the exact env-var syntax against current Claude Code docs since config formats do change.
3. **If not, and an `mcp-builder` skill is available**, use it for the actual scaffolding — it covers FastMCP/Node SDK tool design, auth, and error handling in more depth than belongs here. This skill's job is deciding *whether* to build one and wiring it into the project; treat detailed server implementation as that skill's job, not a second copy of it here.
4. **Add only the tools that will actually be used** — a server with 20 speculative tools is worse than one with the 3 the user needs. Confirm the tool list with the user rather than guessing at full API coverage.
5. **Wire secrets through environment variables.** Never hardcode API keys or tokens in the config file or committed code, even temporarily "to test."
6. **Verify end to end** — connect, call one tool, and show the actual output. Don't declare it working without proof.
7. **Document each tool in one line** so future sessions on this repo know when to reach for it, without having to re-read the server's source.
