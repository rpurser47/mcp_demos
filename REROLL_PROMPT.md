# Reroll Prompt: Weather Chatbot App Recreation

## Objective
Recreate a robust, maintainable Streamlit-based weather chatbot from scratch using python 3.13. The app should:
- Use Streamlit for the chat UI.
- Use a local Llama 3.2 model via Ollama for LLM responses.
- Integrate a weather tool that fetches live weather data from the MCP server (which proxies the National Weather Service API).
- Support tool-calling, so the LLM can invoke the weather tool for live data.
- Use LangGraph for workflow orchestration (multi-node, robust tool-calling, and state management).
- Store the system prompt in an external markdown file for easy editing.
- Be easy to debug, extend, and maintain.

## Requirements
- Reliable tool-calling: LLM should output a special tag (e.g., <<CALL_WEATHER location=...>>) for weather queries, which triggers the weather tool.
- After tool call, the LLM should use the tool result to answer the user.
- Good error handling and debug logging.
- README and requirements.txt for setup.

## Deliverables
- Clean, working codebase with the above features.
- All code should be immediately runnable and easy to extend.
- All instructions and prompts should be clear and up-to-date.

## Notes
- Use latest best practices for Streamlit, Ollama, and LangGraph.
- Make the user experience smooth and the codebase easy to maintain or extend.
