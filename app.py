import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Chat History Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# Sidebar
# ======================
with st.sidebar:
    st.title("Settings")

    model_name = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100
    )

    st.divider()

    if st.button(" Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Chat History")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.expander(
                f"{msg['content'][:30]}..."
            ):
                st.write(msg["content"])

# ======================
# Main Page
# ======================
st.title(" My AI Chatbot")
# Show Old Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Ask anything...")

if user_input:

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Show User Message
    with st.chat_message("user"):
        st.write(user_input)

    try:

        response = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        ai_response = response.choices[0].message.content

    except Exception as e:
        ai_response = f"Error: {str(e)}"

    # Show AI Message
    with st.chat_message("assistant"):
        st.write(ai_response)

    # Save AI Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )
