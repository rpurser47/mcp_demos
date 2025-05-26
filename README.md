# Weather Chatbot (Llama 3.2 + MCP)

A robust, maintainable Streamlit-based weather chatbot powered by local Llama 3.2 via Ollama and live weather data from your MCP server (National Weather Service API).

## Features
- Natural chat interface with Streamlit
- Local Llama 3.2 model (Ollama)
- Tool-calling for live weather (via MCP server)
- Modular, easy-to-extend codebase (LangGraph)

## Setup
1. Install Python 3.13+
2. Clone this repo
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start your MCP server (see `mcp_nws` directory)
5. Start Ollama with Llama 3.2 model:
   ```
   ollama run llama3.2
   ```
6. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

## Configuration
- Edit `chatbot_system_prompt.md` to change the chatbot's behavior.
- All weather queries require the MCP server running on `localhost:8000`.

## Usage
- Ask about the weather in any US location.
- The bot will call the weather tool for live data and answer based on the result.

---

## What You'll Find Here
- **MCP Server**: A FastAPI-based server that provides structured access to current and forecast weather data from the NWS, with endpoints designed for both LLMs and traditional applications.
- **Demo Application**: (Optional/future) A conversational interface where users can ask about the weather in natural language, with the LLM leveraging the MCP server for live data.
- **Learning Focus**: This project is intended as a practical introduction to MCP concepts, showing how external APIs can be made accessible to LLMs and other intelligent agents.

## Project Structure
- `mcp_nws/` — Contains all code, the detailed API README, and implementation for the MCP server.
- `PLAN.md` — The project plan and design rationale.

## Getting Started

### 1. Download and Install Ollama (for Llama 2)
- Visit [https://ollama.com/download](https://ollama.com/download) and follow the instructions for your operating system.
- After installation, open a terminal and run:
  ```sh
  ollama pull llama2
  ```
  This will download the Llama 2 model for local use.

### 2. Start the Ollama Server
- In a terminal, run:
  ```sh
  ollama serve
  ```
  This will start the Ollama server on `localhost:11434` (the default port).

### 3. Start the MCP Server
- In your project root, start the MCP server (FastAPI/Uvicorn) with:
  ```sh
  uvicorn mcp_nws.main:app --reload
  ```
  This will start the MCP server on `localhost:8000`.

### 4. Start the Demo App (Streamlit)
- In your project root, run:
  ```sh
  streamlit run streamlit_app.py
  ```
  The app will be available at [http://localhost:8501](http://localhost:8501).

For setup instructions, API endpoint documentation, and usage examples, see:

👉 **[mcp_nws/README.md](./mcp_nws/README.md)**

This file contains everything you need to run, test, and extend the MCP server.

---

For a detailed breakdown of the project goals, see [PLAN.md](./mcp_nws/PLAN.md).
