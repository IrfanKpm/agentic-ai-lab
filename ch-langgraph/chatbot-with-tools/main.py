from typing import Annotated, TypedDict
from pprint import pprint
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
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
def tool_calling_llm(state: State):
    return {"messages": llm_agent.invoke(state["messages"])}

# Graph-React architecture
graph_builder = StateGraph(State)  
# Creates a new state graph using the defined State schema.
# This is the main container where all nodes and edges are added.
graph_builder.add_node("llm", tool_calling_llm)  
# Adds a node named "llm".
# This node runs the function tool_calling_llm, which calls the LLM with tools enabled.
graph_builder.add_node("tools", ToolNode(tools))  
# Adds a "tools" node.
# ToolNode automatically executes tools (like TavilySearch, get_weather) when requested by the LLM.
graph_builder.add_edge(START, "llm")  
# Defines the entry point of the graph.
# Execution starts from START and goes to the "llm" node first.
graph_builder.add_conditional_edges(
    "llm",
    tools_condition,
)  
# Adds conditional routing after the LLM node.
# tools_condition checks:
# - If tool call is needed → go to "tools" node
# - If no tool needed → go to END (or final response path)
graph_builder.add_edge("tools", "llm")  
# After a tool executes, return back to the LLM node.
# This allows the model to use tool output and continue reasoning.
graph_builder.add_edge("llm", END)  
# If the LLM produces a final answer (no more tool calls), end the graph execution.
# Compile graph
graph = graph_builder.compile()  
# Final step: compiles the graph into an executable LangGraph object.
# After this, you can call graph.invoke(), graph.stream(), etc.

# Visualize the Graph
def visualGraph():
    image = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(image)

# Run once to generate graph.png, then keep disabled unless the graph changes.
#visualGraph()


# Q1
response1 = graph.invoke({"messages": [("user", "what is latest AI news")]})
pprint(response1["messages"][-1].content)

# Q2
response2 = graph.invoke({"messages": [("user", "weather status in mumbai")]})
pprint(response2["messages"][-1].content)