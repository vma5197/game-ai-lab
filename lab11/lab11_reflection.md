# Lab 11 Reflection

## Task 1: Demo Exploration

### What method is called first when a client connects to a server?
`initialize` is called first. It performs a handshake exchanging protocol version, capabilities, and client/server identity before any tools can be used.

### What information does `tools/list` return?
It returns a list of tool objects, each with a `name`, `description`, and `inputSchema` (a JSON Schema describing the expected arguments and which are required).

### What is the structure of a `tools/call` request?
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add_numbers",
    "arguments": { "a": 5, "b": 3 }
  }
}

---

## Task 4: Reflection

### 1. MCP + LangGraph vs. Lab 05 Manual Tool Calling

In Lab 05, tool calling was handled manually. After the model responded, we had to check `response.message.tool_calls`, loop over each call, execute the function with `process_function_call()`, manually append the result back into `self.messages` with the correct role and fields, and then re-call `self.completion()` to continue. This loop had to be written by hand and was tightly coupled to Ollama's specific message format.

With MCP + LangGraph, all of that is handled automatically. `load_mcp_tools()` converts the MCP server's tools into LangChain-compatible tools, and `create_react_agent` runs the full tool-calling loop internally — no manual message appending or re-querying needed. MCP also makes the tools reusable across any MCP-compatible host, not just one custom implementation.

### 2. MCP Enhancement for the DnD Dungeon Master Project

A natural addition would be wrapping the existing `roll_for` function from Lab 05 as an MCP tool. Currently it's a plain Python function called manually inside the agent loop. Exposing it through an MCP server means the DM agent can call it through the standard protocol, and the same dice-rolling server could be reused by other agents without duplicating code.

---

## Task 1 Demo Output

======================================================================
                    MCP Protocol Demo
======================================================================

Connecting to server: simple_mcp_server.py

This demo shows the actual MCP protocol messages that flow
between client and server using JSON-RPC format.

######################################################################
# STEP 1: Initialize Connection
######################################################################

  CLIENT -> SERVER  |  initialize (request)
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": { "tools": {} },
    "clientInfo": { "name": "demo-client", "version": "1.0.0" }
  }
}

  SERVER -> CLIENT  |  initialize (response)
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "serverInfo": { "name": "demo-server", "version": "1.0.0" },
    "capabilities": { "tools": { "listChanged": true } }
  }
}

[OK] Connection initialized!

######################################################################
# STEP 2: List Available Tools
######################################################################

  CLIENT -> SERVER  |  tools/list (request)
{ "jsonrpc": "2.0", "method": "tools/list", "params": {} }

  SERVER -> CLIENT  |  tools/list (response)
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "get_current_time",
        "description": "Returns the current date and time",
        "inputSchema": { "type": "object", "properties": { "timezone": { "type": "string" } }, "required": [] }
      },
      {
        "name": "add_numbers",
        "description": "Adds two numbers together",
        "inputSchema": { "type": "object", "properties": { "a": { "type": "number" }, "b": { "type": "number" } }, "required": ["a", "b"] }
      }
    ]
  }
}

[OK] Found 2 tools!

######################################################################
# STEP 3: Call Tool - get_current_time
######################################################################

  CLIENT -> SERVER  |  tools/call (request)
{ "jsonrpc": "2.0", "method": "tools/call", "params": { "name": "get_current_time", "arguments": {} } }

  SERVER -> CLIENT  |  tools/call (response)
{ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": "Current time: 2025-04-06 14:23:11" }] } }

[OK] Tool result: Current time: 2025-04-06 14:23:11

######################################################################
# STEP 4: Call Tool with Arguments - add_numbers(5, 3)
######################################################################

  CLIENT -> SERVER  |  tools/call (request)
{ "jsonrpc": "2.0", "method": "tools/call", "params": { "name": "add_numbers", "arguments": { "a": 5, "b": 3 } } }

  SERVER -> CLIENT  |  tools/call (response)
{ "jsonrpc": "2.0", "result": { "content": [{ "type": "text", "text": "5 + 3 = 8" }] } }

[OK] Tool result: 5 + 3 = 8