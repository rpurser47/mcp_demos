# Overall Plan for MCP Weather Demo

_I want to learn about model context protocol by creating an example MCP that gives access to the national weather service and a demo application that uses an LLM with that MCP to have a conversation about the current and future weather locally._

---

Great! Here’s a high-level plan for your learning project, which will help you understand Model Context Protocol (MCP) by building a practical example:

## Project Overview
1. **Create an MCP server** that exposes the National Weather Service (NWS) API as a resource.
2. **Build a demo application** that uses a local Llama 2 model (via Ollama) and LangChain to provide a conversational interface about local weather, fetching live/current and forecast data from the MCP server through tool-calling.
3. **Demonstrate how the LLM interacts with the MCP** to answer user questions about the weather.

## Step-by-Step Breakdown
1. MCP Server for National Weather Service
  - Goal: Wrap the NWS API in an MCP-compliant server.
  - Features:
    - Expose endpoints for current weather and forecasts.
    - Accept location input (city, zip, or lat/lon).
    - Accept date input (ISO date, "today", "tomorrow", or weekday name).
    - Return weather data in a structured format (JSON).
2. Demo Application
  - Goal: Build a simple chat interface (web-based, using Streamlit) where a user can ask about the weather.
  - Features:
    - User asks questions like “What’s the weather in Boston?” or “Will it rain tomorrow in San Francisco?”
    - The app uses a local Llama 2 model (run via Ollama) orchestrated by LangChain to interpret the request.
    - The LLM uses LangChain tool-calling to invoke the MCP server endpoints for weather data as needed.
    - The LLM generates a conversational response using the live weather data.
    - The chat interface is implemented in Streamlit for rapid prototyping and modern UX, with explicit support for dark mode.
    - Ollama is used as the backend for running the Llama 2 model locally.
3. Learning Outcomes
  - Understand how MCP abstracts access to external APIs.
  - See how LLMs can leverage MCP resources for real-world tasks.
  - Gain hands-on experience with both backend (MCP server) and frontend (chat app with LLM).
