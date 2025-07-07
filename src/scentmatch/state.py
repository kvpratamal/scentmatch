from typing import Dict
from langgraph.graph import MessagesState


class WorkflowState(MessagesState):
    about_user: Dict[str, str]
    sales_pitch: str


class WorkflowStateInput(MessagesState):
    about_user: Dict[str, str]


class WorkflowStateOutput(MessagesState):
    sales_pitch: str
