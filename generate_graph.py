"""
Script to generate and save the LangGraph agent's graph as an image.
"""
from graph_flow import build_graph
from llm_agent import get_llms

if __name__ == "__main__":
    raw_llm, llm, summarize_email = get_llms()
    graph = build_graph(llm, summarize_email)
    nx_graph = graph.get_graph()
    nx_graph.draw_png('agent_graph.png')
    print("Graph saved as agent_graph.png")
