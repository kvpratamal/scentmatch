from langgraph.graph import START, StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from scentmatch.state import (
    WorkflowState,
    WorkflowStateInput,
    WorkflowStateOutput,
    ChatWorkflowState,
    ChatWorkflowStateInput,
    ChatWorkflowStateOutput,
)
from scentmatch.nodes import sales_node, chat_node
from scentmatch.configuration import Configuration

# Build the sales graph
builder = StateGraph(
    WorkflowState,
    input=WorkflowStateInput,
    output=WorkflowStateOutput,
    config_schema=Configuration,
)

builder.add_node("sales_node", sales_node)

builder.add_edge(START, "sales_node")
builder.add_edge("sales_node", END)

graph = builder.compile()

# Build the chat graph
chat_builder = StateGraph(
    ChatWorkflowState,
    input=ChatWorkflowStateInput,
    output=ChatWorkflowStateOutput,
    config_schema=Configuration,
)

chat_builder.add_node("chat_node", chat_node)

chat_builder.add_edge(START, "chat_node")
chat_builder.add_edge("chat_node", END)

checkpointer = InMemorySaver()
chat_graph = chat_builder.compile(checkpointer=checkpointer)
