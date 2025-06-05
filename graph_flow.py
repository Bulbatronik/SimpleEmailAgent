"""
Graph construction and flow logic for the agent.
"""
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from llm_agent import ChatState, llm_node
from email_tools import list_unread_email

def router(state):
    last_message = state['messages'][-1]
    return 'tools' if getattr(last_message, 'tool_calls', None) else 'end'

def build_graph(llm, summarize_email):
    tool_node = ToolNode([list_unread_email, summarize_email])
    def tools_node(state):
        result = tool_node.invoke(state['messages'])
        # Ensure result is wrapped as a message dict
        if isinstance(result, dict) and 'role' in result and 'content' in result:
            message = result
        else:
            message = {'role': 'assistant', 'content': str(result)}
        return {
            'messages': state['messages'] + [message],
        }
    builder = StateGraph(ChatState)
    builder.add_node('llm', llm_node(llm))
    builder.add_node('tools', tools_node)
    builder.add_edge(START, 'llm')
    builder.add_edge('tools', 'llm')
    builder.add_conditional_edges('llm', router, {'tools': 'tools', 'end': END})
    return builder.compile()
