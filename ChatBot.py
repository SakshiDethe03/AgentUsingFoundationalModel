import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from pprint import pprint

model = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = create_agent(model=model)

def get_lc_messages(chat_history):
    """
    Convert Streamlit chat format → LangChain format
    """
    lc_messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    return lc_messages


def stream_response(chat_history):
    """
    Stream response from agent
    """
    lc_messages = get_lc_messages(chat_history)

    for token, metadata in agent.stream(
        {"messages": lc_messages},
        stream_mode="messages"
    ):
        if token.content:
            yield token.content