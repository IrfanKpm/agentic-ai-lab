from typing import Annotated,TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import START,END
from langgraph.graph.message import add_messages  # message reducer for appending chat messages

from langchain.chat_models import init_chat_model

import settings


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


llm = init_chat_model("gpt-4o-mini",model_provider="openai"
)
