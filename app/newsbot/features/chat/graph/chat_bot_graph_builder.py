import logging
from enum import Enum

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.runnables import Runnable 
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.tools import BaseTool

from IPython.display import display, Image

from ..state.chat_state import ChatState
from ..node.chat_bot import ChatBotNode

logger = logging.getLogger(__name__)

class NodeId(str, Enum):
    CHAT_BOT = "chat_bot"
    TOOLS_NODE = "tools_node"


class ChatBotGraphBuilder:
    """Builds a state graph for the chatbot application."""

    def __init__(self, llm: Runnable, tools: list[BaseTool]):
        self.llm = llm
        self.tools = tools

    def build(self) -> Runnable:
        graph_builder = StateGraph(ChatState)

        # Add chat bot node
        chatbotNode = ChatBotNode(llm=self.llm)
        graph_builder.add_node(NodeId.CHAT_BOT.value, chatbotNode.chatbot)
        
        # Add tool node only if tools are available
        if self.tools:
            tool_node = ToolNode(tools=self.tools)
            graph_builder.add_node(NodeId.TOOLS_NODE.value, tool_node)

        # Add edges
        graph_builder.add_edge(START, NodeId.CHAT_BOT.value)
        
        if self.tools:
            # With tools: chat → tools → chat flow
            graph_builder.add_conditional_edges(
                NodeId.CHAT_BOT.value,
                tools_condition,
                {"tools": NodeId.TOOLS_NODE.value, END: END},
            )
            graph_builder.add_edge(NodeId.TOOLS_NODE.value, NodeId.CHAT_BOT.value)
        else:
            # Without tools: direct chat → end
            graph_builder.add_edge(NodeId.CHAT_BOT.value, END)

        # Compile with memory
        memory = InMemorySaver()
        app = graph_builder.compile(checkpointer=memory)

        # Visualization
        try:
            image = app.get_graph().draw_mermaid_png()
            display(Image(image))
        except Exception as e:            
            logger.info(f"Error details: {e}")
            logger.info(app.get_graph().draw_mermaid())

        return app
