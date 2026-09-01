from agents import retrieve_knowledge
from graph import AgentState

def knowledge_node(state: AgentState) -> dict:
    docs = retrieve_knowledge(state.customer_message, k=3)

    return {
        "knowledge": docs,
    }