import streamlit as st
from ChatBot import stream_response

# Page config
st.set_page_config(page_title="Groq Chatbot", layout="wide")
st.title("💬 Groq Chatbot")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask something...")

if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in stream_response(st.session_state.messages):
            full_response += chunk
            response_container.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })  