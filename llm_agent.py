"""
LLM initialization, tool binding, and agent logic.
"""
from typing import TypedDict
from langchain.chat_models import init_chat_model
from config import CHAT_MODEL
from email_tools import list_unread_email, summarize_email_factory


def get_llms():
    raw_llm = init_chat_model(CHAT_MODEL, model_provider='ollama')
    summarize_email = summarize_email_factory(raw_llm)
    llm = raw_llm.bind_tools([list_unread_email, summarize_email])
    return raw_llm, llm, summarize_email


class ChatState(TypedDict):
    messages: list


def llm_node(llm):
    def node(state):
        response = llm.invoke(state['messages'])
        return {
            'messages': state['messages'] + [response]
        }
    return node
