from agents import investigate
from graph.state import AgentState
 
def investigation_node(state: AgentState) -> dict:
    result = investigate(
        customer_message=state.customer_message,
        customer_id=state.customer_id or "unknown",
    )
 
    return {
        "investigation": result,
    }