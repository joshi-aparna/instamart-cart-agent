# Swiggy Instamart Cart Agent

An LLM-powered shopping cart agent that interacts with Swiggy Instamart through its remote Model Context Protocol (MCP) server.

This project explores building practical AI agents that interact with real-world services. It uses LangChain for agent orchestration, structured inputs and outputs for reliable application integration, and configurable LLMs for reasoning and tool execution.

## What it does

The Instamart agent currently supports:

- **Add items:** Search for products and add matching products to the Instamart cart.
- **View cart:** Retrieve the current cart contents.
- **Cart value:** Retrieve the cart's current value.
- **Clear cart:** Remove items from the cart.

The agent manages the shopping cart only. It does not place orders or make payments.

## Architecture

The agent is part of a larger shopping assistant workflow. A message interpreter extracts shopping intent and converts it into structured input. A command router directs the request to the appropriate component.

```text
User Request
     |
     v
Message Interpreter
     |
     v
ShoppingItems (structured output)
     |
     v
Command Router
     |
     +---- cartadd
     |        |
     |        v
     |    Instamart Agent
     |        |
     |        v
     |    LangChain Agent
     |        |
     |        v
     |    Instamart MCP Server
     |
     +---- listadd
              |
              v
          Notion
```

The Instamart agent is responsible for cart operations. It uses an LLM to select and invoke the relevant MCP tools.

The agent is intentionally independent of the message interpreter and shopping list management components.

## Technology

- **Python** – Agent implementation.
- **LangChain / LangGraph** – Agent orchestration and tool execution.
- **Model Context Protocol (MCP)** – Integration with Instamart's remote tools.
- **Pydantic** – Structured input and output models.
- **LLM Gateway** – Model selection, provider routing and fallback.
- **Ollama** – Local model execution and fallback.
- **Authlib / Cryptography** – OAuth authentication and encrypted token storage.

## Engineering decisions and learnings

### 1. Don't expose every MCP tool to the LLM

An MCP server can expose many tools, but that doesn't mean an agent should have access to all of them.

Exposing too many tools increases the complexity of tool selection and can lead to unnecessary or incorrect tool calls.

The agent uses a curated set of tools relevant to its responsibilities.

### 2. Treat tool descriptions and results carefully

Tool descriptions can contain instructions that influence model behaviour. Tool responses can also contain text that looks like instructions.

This makes it important to establish clear boundaries between system instructions, tool metadata, tool results and user intent.

### 3. Use structured responses

The agent uses Pydantic models to represent operation results instead of relying entirely on conversational text.

Structured responses make it easier for the calling application to consume results reliably.

### 4. Keep agent responsibilities narrow

The Instamart agent manages cart operations. It does not interpret the entire shopping workflow, manage shopping lists or place orders.

Those responsibilities belong to other components.

Keeping responsibilities separate makes the agent easier to reason about, test and evolve.

### 5. Bound agent execution

Tool execution does not always proceed as expected. A tool may report success for one operation while a subsequent operation continues to fail.

Agent iteration limits are important to prevent repeated tool calls, infinite loops and unnecessary API consumption.

### 6. Model selection matters

Not every model is equally capable of following tool-calling instructions or producing reliable structured outputs.

The project explores model routing and fallback across different providers, rather than assuming that any model can be substituted without affecting agent behaviour.

## Scope and limitations

- Cart management only.
- Requires Instamart MCP authentication.
- Requires the configured LLM provider to be available.
- Product matching and tool execution depend on the underlying Instamart MCP implementation.
- No checkout, order placement or payment functionality.

## Development

This is an experimental project exploring practical AI agent engineering, MCP integrations, tool orchestration, structured outputs and model routing.

The implementation and architecture continue to evolve as new patterns, limitations and failure modes are explored.