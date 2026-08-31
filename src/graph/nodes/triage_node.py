from agents import triage_agent
from graph import AgentState
 
def triage_node(state: AgentState) -> dict:
    result = triage_agent(state.customer_message)
 
    return {
        "intent": result.intent,
        "priority": result.priority,
    }