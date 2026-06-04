from typing import Annotated, TypedDict
from pprint import pprint
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver 
from langchain_core.messages import SystemMessage


from langchain_tavily import TavilySearch
import settings

# State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# LLM
llm = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0,
)

# Tools
search_tool = TavilySearch(max_results=2)

def get_weather(city: str) -> str:
    """
    Get current weather for a specific CITY name (e.g., 'kochi', 'mumbai', 'london')
    Args:
        city (str): Name of the city
    Returns:
        str: Weather description for the city
    """
    weather_data = {
        "kochi": "32°C, Humid 🌤️",
        "mumbai": "35°C, Hot ☀️",
        "london": "12°C, Cloudy 🌧️",
    }
    return weather_data.get(city.lower(), "Weather data not found")

tools = [search_tool, get_weather]

# Bind tools to LLM
llm_agent = llm.bind_tools(tools)

# Node function

SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful assistant. Always respond in natural language."
)

def tool_calling_llm(state: State):
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = llm_agent.invoke(messages)
    return {"messages": response}

memory = MemorySaver()


graph_builder = StateGraph(State)  
graph_builder.add_node("llm", tool_calling_llm)  
graph_builder.add_node("tools", ToolNode(tools))  
graph_builder.add_edge(START, "llm")  
graph_builder.add_conditional_edges(
    "llm",
    tools_condition,
)  
graph_builder.add_edge("tools", "llm")  
graph_builder.add_edge("llm", END)  

graph = graph_builder.compile(checkpointer=memory)  


config = {
    "configurable": {
        "thread_id": "1"
    }
}

## STREAM 

# --> stream() | astream()
 
print("========= stream_mode=updates =======")
for chunk in graph.stream({"messages": [("user", "what's the weather in Kochi")]},config=config,stream_mode="updates"):
    pprint(chunk)

print("\n========= stream_mode=values =======")
for chunk in graph.stream({"messages": [("user", "what's the weather in Kochi")]},config=config,stream_mode="values"):
    pprint(chunk)

print("\n\n========= stream_mode=messages =======")
for chunk in graph.stream({"messages": [("user", "what's the weather in Kochi")]},config=config,stream_mode="messages"):
    pprint(chunk)


