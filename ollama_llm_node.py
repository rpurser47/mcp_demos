import ollama

def ollama_llm_node(state):
    """
    LangGraph node for calling the local Llama 3.2 model via Ollama.
    Expects state dict with keys:
      - 'input': user prompt (str)
      - 'system_prompt': system prompt (str)
    Returns updated state with 'output' key (str).
    """
    prompt = state.get("input", "")
    system_prompt = state.get("system_prompt", "")
    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    output = response["message"]["content"]
    # Print only the assistant's reply, not the full state or prompt
    import json
    raw_output = output
    if isinstance(output, str) and output.strip().startswith("{"):
        try:
            parsed = json.loads(output)
            # Try common keys for the assistant's reply
            for key in ["assistant", "content", "output", "reply", "message"]:
                if key in parsed:
                    raw_output = parsed[key]
                    break
            else:
                # If none of the above keys, just print the whole parsed object
                raw_output = str(parsed)
        except Exception:
            pass  # If not JSON, leave as is
    print("[DEBUG] LLM raw output:", raw_output)
    state = dict(state)
    state["output"] = output
    return state
