import logging

from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage

from ..state.chat_state import ChatState

logger = logging.getLogger(__name__)


class ChatBotNode:
    """Chat node for processing user queries and generating AI responses."""
    
    def __init__(self, llm: Runnable) -> None:
        self.llm = llm

    def chatbot(self, state: ChatState) -> dict:
        """Process chat messages and generate a response."""
        logger.info("ChatBot node processing user query")

        try:
            query = state.get("query", "")
            messages = state.get("messages", [])

            # Validate query
            if not query.strip():
                logger.warning("Empty query received")
                return {"messages": [AIMessage(content="I didn't receive a question. How can I help you?")]}

            if messages:
                messages.append(HumanMessage(content=query))
            else:
                messages = [
                    SystemMessage(
                        content="""
                        You are a helpful and knowledgeable AI assistant. Your role is to:
                        
                        1. Answer user questions clearly and accurately
                        2. Use available tools when they can help provide better information
                        3. If tools are not available, rely on your training knowledge
                        4. Admit when you don't know something rather than guessing
                        5. Keep responses concise but comprehensive
                        6. Be friendly and professional in tone
                        
                        When using tools, explain what you're doing to help the user understand.
                        """
                    ),
                    HumanMessage(content=query),
                ]

            # Generate response using LLM
            response = self.llm.invoke(messages)
            logger.debug(f"Response content preview: {str(response)[:100]}...")
            
            return {"messages": [response]}
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error while processing your request: {str(e)}"
            logger.error(f"ChatBot node error: {e}", exc_info=True)
            return {"messages": [AIMessage(content=error_msg)]}
