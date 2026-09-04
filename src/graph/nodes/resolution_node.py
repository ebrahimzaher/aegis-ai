from agents import resolve
from graph import AgentState

def resolution_node(state: AgentState) -> dict:
    result = resolve(
        customer_message=state.customer_message,
        retrieved_docs=state.retrieved_docs,
        investigation=state.investigation,
        policy_check=state.policy_check,
    )

    return {
        "resolution": result,
    }