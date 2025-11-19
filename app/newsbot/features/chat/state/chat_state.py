from typing import Annotated, NotRequired
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages, BaseMessage


class ChatState(TypedDict):
    """
    State representation for the chat application using LangGraph.
    
    This TypedDict defines the structure of state that flows through
    the chat workflow graph nodes.
    
    Fields:
        query: The current user input/question to be processed
        messages: Optional conversation history with automatic message
                 accumulation via add_messages annotation
    """
    query: str
    messages: NotRequired[Annotated[list[BaseMessage], add_messages]]