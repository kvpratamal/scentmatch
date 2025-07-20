from typing import Dict
from langgraph.graph import MessagesState


class WorkflowState(MessagesState):
    about_user: Dict[str, str]
    sales_pitch: str
    chosen_product: str


class WorkflowStateInput(MessagesState):
    about_user: Dict[str, str]


class WorkflowStateOutput(MessagesState):
    sales_pitch: str
    chosen_product: str


class ChatWorkflowState(MessagesState):
    question: str
    product: str
    response: str


class ChatWorkflowStateInput(MessagesState):
    question: str
    product: str


class ChatWorkflowStateOutput(MessagesState):
    response: str
