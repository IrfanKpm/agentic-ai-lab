from typing import Annotated,TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import START,END
from langgraph.graph.message import add_messages  # message reducer for appending chat messages

from langchain.chat_models import init_chat_model

import settings


class State(TypedDict):
    messages: Annotated[list, add_messages]




llm = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0,
)

# Node Functionality
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Graph Setup
graph_builder = StateGraph(State)
graph_builder.add_node("llmChatbot",chatbot) # (node_name,node_fucntion)
graph_builder.add_edge(START,"llmChatbot")
graph_builder.add_edge("llmChatbot",END)

# Graph Compile
graph = graph_builder.compile()

# Visualize the Graph
def visualGraph():
    image = graph.get_graph().draw_png()
    with open("graph.png", "wb") as f:
        f.write(image)

visualGraph()