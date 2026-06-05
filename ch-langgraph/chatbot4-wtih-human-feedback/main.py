from typing import Annotated, TypedDict
from pprint import pprint

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

import settings

# State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# llm
llm = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    temperature=0,
)

# Human Tool
@tool
def human_assistance(query: str) -> str:
    """
    Request approval/help from a human.
    """
    human_response = interrupt(
        {
            "question_for_human": query
        }
    )
    return human_response["data"]

tools = [human_assistance]
llm_with_tools = llm.bind_tools(tools)

# Chatbot Node
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# GRAPH
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot",tools_condition)
graph_builder.add_edge("tools","chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Visualize the Graph
def visualGraph():
    image = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(image)


# Run once to generate graph.png,
# then disable unless graph changes.
visualGraph()


# Config
config = {
    "configurable": {
        "thread_id": "1"
    }
}


# First Execution
result = graph.invoke(
    {
        "messages": [
            (
                "user",
                "Use human assistance and ask whether my refund should be approved."
            )
        ]
    },
    config=config
)

print("\n" + "=" * 60)
print("FIRST EXECUTION")
print("=" * 60)

pprint(result)


# Human Approval Flow
if "__interrupt__" in result:

    print("\n" + "=" * 60)
    print("HUMAN REVIEW REQUIRED")
    print("=" * 60)

    interrupt_data = result["__interrupt__"][0].value

    question = interrupt_data["question_for_human"]

    print(f"\nQuestion: {question}")

    while True:

        approval = input(
            "\nApprove? (yes/no): "
        ).strip().lower()

        if approval in ["yes", "y"]:
            human_response = "Approved by human reviewer."
            break

        elif approval in ["no", "n"]:
            human_response = "Rejected by human reviewer."
            break

        print("Please enter 'yes' or 'no'.")


    result = graph.invoke(
        Command(
            resume={
                "data": human_response
            }
        ),
        config=config
    )

    print("\n" + "=" * 60)
    print("FINAL RESPONSE")
    print("=" * 60)

    pprint(result["messages"][-1].content)