"""
Entry point for the CLI agent. Handles user interaction and state management.
"""
from llm_agent import get_llms
from graph_flow import build_graph


if __name__ == "__main__":
    raw_llm, llm, summarize_email = get_llms()
    graph = build_graph(llm, summarize_email)
    state = {'messages': []}  # Initialize the state with an empty messages list
    
    print('Type instruction or "quit".\n')
    
    while True:
        user_message = input('> ')
        
        if user_message.lower() == 'quit':
            break
            
        state['messages'].append({'role': 'user', 'content': user_message})
        
        state = graph.invoke(state)
        
        print(state['messages'][-1].content)
