from typing import List, Dict
from langgraph.graph import MessagesState

# Define the state type with annotations
class WorkflowState(MessagesState):
    system_message: str
    about_user: List[Dict[str, str]]
    final_answer: str

class WorkflowStateInput(MessagesState):
    system_message: str
    about_user: List[Dict[str, str]]

class WorkflowStateOutput(MessagesState):
    final_answer: str