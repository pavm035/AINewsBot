import streamlit as st
from langchain_core.runnables import RunnableConfig

from newsbot.core import SessionConfig
from newsbot.features import ChatBotAgent, ChatState

class ChatUIManager:
    def __init__(self, session_config: SessionConfig):
        self.session_config = session_config

    def start_chat(self):
        """Start the chat interface using Streamlit."""
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        if "agent" not in st.session_state:
            st.session_state.agent = None

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?"):
            # ✅ Validate API key ONLY when user sends first message
            if not self.session_config.llm_api_key:
                st.error("❌ Please enter your GROQ API key in the sidebar first!")
                st.stop()

            # Create a config key to detect changes
            parts = [
                self.session_config.selected_llm_provider.value if self.session_config.selected_llm_provider else "",
                self.session_config.selected_model,
                self.session_config.selected_usecase.value if self.session_config.selected_usecase else "",
            ]
            current_config_key = "_".join(parts)

            # Check if we need to recreate agent due to config changes
            if st.session_state.get("config_key") != current_config_key:
                st.session_state.messages = []

                with st.spinner("🔧 Initializing chatbot..."):
                    try:
                        agent_builder = ChatBotAgent(session_config=self.session_config)
                        st.session_state.agent = agent_builder.create_agent()
                        st.session_state.config_key = current_config_key
                        st.success("Chatbot ready!", icon="✅")
                    except Exception as e:
                        st.error(f"❌ Failed to initialize: {str(e)}")
                        st.stop()

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Generate response
            with st.chat_message("assistant"):
                # Generate unique thread ID
                if "thread_id" not in st.session_state:
                    import uuid

                    st.session_state.thread_id = str(uuid.uuid4())

                config: RunnableConfig = {
                    "configurable": {"thread_id": st.session_state.thread_id}
                }

                with st.spinner("Thinking... 🤔"):            

                    state = ChatState(query=prompt)
                    agent = st.session_state.agent
                    if agent is None:
                        st.error("⚠️ Agent is not initialized.")
                        st.stop()

                    response = agent.invoke(state, config=config)

                # Extract assistant message
                final_messages = response.get("messages", [])
                assistant_message = None

                for msg in reversed(final_messages):
                    if hasattr(msg, "content") and msg.content:
                        if not hasattr(msg, "type") or msg.type != "tool":
                            assistant_message = msg.content
                            break

                if assistant_message:
                    st.markdown(assistant_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                    )
                else:
                    error_msg = "I couldn't generate a response."
                    st.markdown(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )
