from langgraph.graph import START, StateGraph, END
from scentmatch.state import WorkflowState, WorkflowStateInput, WorkflowStateOutput
from scentmatch.nodes import sales_node
from scentmatch.configuration import Configuration

# Build the graph
builder = StateGraph(WorkflowState, input=WorkflowStateInput, output=WorkflowStateOutput, config_schema=Configuration)
builder.add_node("sales_node", sales_node)
builder.add_edge(START, "sales_node")
builder.add_edge("sales_node", END)

graph = builder.compile()
