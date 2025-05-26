import re
from ollama_llm_node import ollama_llm_node
from weather_tools import get_weather

def llm_router_node(state):
    """
    Decides if the LLM output indicates a tool call. If so, routes to 'get_weather'.
    Otherwise, routes to END.
    Expects state with 'output' from LLM.
    Adds 'tool_args' to state if tool should be called.
    """
    import re
    output = state.get("output", "")
    print("[DEBUG] LLM output in router:", output)
    # Match the tool call and extract all key=value pairs
    match = re.search(r"<<CALL_WEATHER(.*?)>>", output)
    tool_args = {}
    if match:
        args_str = match.group(1)
        # Find all key=value pairs, allowing for spaces
        for key, value in re.findall(r"(\w+)=([^\s>]+)", args_str):
            tool_args[key] = value
        state = dict(state)
        state["tool_args"] = tool_args
        state["tool_call"] = True
        state["next"] = "get_weather"
        print("[DEBUG] llm_router_node return state:", state)
        return state
    else:
        state = dict(state)
        state["tool_call"] = False
        state["next"] = "END"
        print("[DEBUG] llm_router_node return state:", state)
        return state

import ollama
from weather_tools import get_weather

import datetime

def get_dynamic_system_prompt():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"""
Today is {today}.
You are WeatherBot, a helpful assistant specializing in US weather information.
- For any weather-related question, ALWAYS call the weather tool to get up-to-date information from the MCP server.
- Never make up weather data or forecasts. If you cannot access live data, politely inform the user.
- To call the weather tool, output ONLY the following format, including all relevant parameters (such as location, lat, lon, and date):
  <<CALL_WEATHER location=Boston date=tomorrow>>
  <<CALL_WEATHER lat=42.36 lon=-71.06 date=Monday>>
- Do NOT answer weather questions directly or guess. Only answer after receiving the tool result.
- If the user asks a non-weather question, politely redirect them to ask about the weather.
You should always answer in the same language as the user's ask.
"""

def ollama_llm_node(state):
    print("[DEBUG] ollama_llm_node called", flush=True)
    # Prefer multi-turn chat if available
    messages = state.get("messages")
    system_prompt = state.get("system_prompt")
    if not system_prompt:
        system_prompt = get_dynamic_system_prompt()
    # Build the message list for Ollama
    ollama_messages = []
    ollama_messages.append({"role": "system", "content": system_prompt})
    # If prior messages (multi-turn), add them; else, just use current input
    if messages and isinstance(messages, list):
        for msg in messages:
            # Ensure each message is a dict with role/content
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                ollama_messages.append({"role": msg["role"], "content": msg["content"]})
    else:
        user_input = state.get("input", "")
        ollama_messages.append({"role": "user", "content": user_input})
    # If weather_result is present, append as context for the assistant
    weather_result = state.get("weather_result")
    if weather_result:
        ollama_messages.append({"role": "system", "content": f"Weather data: {weather_result}"})
    print("[DEBUG] ollama_llm_node input messages:", ollama_messages)
    response = ollama.chat(
        model="llama3.2:latest",
        messages=ollama_messages
    )
    output = response["message"]["content"]
    print("[DEBUG] ollama_llm_node LLM response:", output)
    state = dict(state)
    state["output"] = output
    # Append LLM response to messages
    messages = state.get("messages", [])
    messages.append({
        "role": "assistant",
        "content": output
    })
    state["messages"] = messages
    return state

def weather_tool_node(state):
    """
    Calls the get_weather tool with arguments from state['tool_args'].
    Adds 'weather_result' to state.
    """
    print("[DEBUG] weather_tool_node state:", state)
    args = state.get("tool_args", {})
    print("[DEBUG] weather_tool_node tool_args:", args)
    result = get_weather(**args)
    state = dict(state)
    state["weather_result"] = result
    # Append tool result to messages
    messages = state.get("messages", [])
    messages.append({
        "role": "system",
        "content": f"Weather data: {result}"
    })
    state["messages"] = messages
    return state
