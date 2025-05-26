import streamlit as st
import requests
from langchain_community.llms.ollama import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate

# --- Load system prompt from file ---
def load_system_prompt():
    with open("chatbot_system_prompt.md", "r", encoding="utf-8") as f:
        return f.read()

system_prompt = load_system_prompt()
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt)
])
from langchain.chains import LLMChain

# --- Streamlit page config ---
st.set_page_config(
    page_title="Weather Chatbot (Llama 2 + MCP)",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("☁️ Weather Chatbot (Llama 3.2 + MCP)")
st.caption("Ask about the weather anywhere in the US. Powered by local Llama 3 via Ollama, LangChain, and your MCP server.")

# --- MCP Weather Tool ---
def get_weather(location: str = None, lat: float = None, lon: float = None, date: str = None):
    """Call the MCP server to get weather data by name or coordinates."""
    if location:
        params = {"location": location}
        if date:
            params["date"] = date
        url = "http://localhost:8000/resources/nws-weather-by-name"
    elif lat is not None and lon is not None:
        params = {"lat": lat, "lon": lon}
        if date:
            params["date"] = date
        url = "http://localhost:8000/resources/nws-weather"
    else:
        return {"status": "error", "message": "Must provide location name or lat/lon."}
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

weather_tool = Tool(
    name="get_weather",
    func=lambda location=None, lat=None, lon=None, date=None: get_weather(location, lat, lon, date),
    description="Get current and forecast weather for a US location (city, state, zip, or lat/lon) and optional date ('today', 'tomorrow', weekday, or ISO date)."
)

# --- Llama 2 via Ollama ---
llm = Ollama(model="llama3.2:latest")

# --- Agent Setup ---
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent="chat-conversational-react-description",
    prompt=prompt,
    verbose=False
)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# --- User input ---
if prompt := st.chat_input("Ask me about the weather..."):
    print(f"[DEBUG] User prompt received: {prompt}")
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("Llama 3.2 is thinking..."):
        # Build conversation history for agent
        conversation = "\n".join([f"User: {m['content']}" if m['role']=='user' else f"Assistant: {m['content']}" for m in st.session_state["messages"] if m["role"] in ("user", "assistant")])
        # Prepare chat history as a list of (role, content) tuples
        chat_history = [
            (m["role"], m["content"])
            for m in st.session_state["messages"]
            if m["role"] in ("user", "assistant")
        ]
        print("[DEBUG] Invoking Llama model via agent...")
        try:
            response = agent.invoke({"input": prompt, "chat_history": chat_history}, handle_parsing_errors=True)
            print(f"[DEBUG] Llama model response: {response}")
            if isinstance(response, dict) and "output" in response:
                response = response["output"]
        except ValueError as e:
            print(f"[ERROR] Agent parsing error: {e}")
            response = "Sorry, I couldn't process that request. Please check your input or try a different location. (Agent parsing error)"
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# --- Dark mode note ---
st.markdown("<style>body { background-color: #18191A !important; color: #fff !important; }</style>", unsafe_allow_html=True)
