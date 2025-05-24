# MCP Weather Demo: High-Level Overview

This project demonstrates a Model Context Protocol (MCP) server that exposes the National Weather Service (NWS) API as a resource, along with a demo application that enables conversational weather queries using an LLM (Large Language Model).

## What You'll Find Here
- **MCP Server**: A FastAPI-based server that provides structured access to current and forecast weather data from the NWS, with endpoints designed for both LLMs and traditional applications.
- **Demo Application**: (Optional/future) A conversational interface where users can ask about the weather in natural language, with the LLM leveraging the MCP server for live data.
- **Learning Focus**: This project is intended as a practical introduction to MCP concepts, showing how external APIs can be made accessible to LLMs and other intelligent agents.

## Project Structure
- `mcp_nws/` — Contains all code, the detailed API README, and implementation for the MCP server.
- `PLAN.md` — The project plan and design rationale.

## Getting Started
For setup instructions, API endpoint documentation, and usage examples, see:

👉 **[mcp_nws/README.md](./mcp_nws/README.md)**

This file contains everything you need to run, test, and extend the MCP server.

---

For a detailed breakdown of the project goals, see [PLAN.md](./mcp_nws/PLAN.md).
