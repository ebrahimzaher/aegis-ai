from agents import check_policy
from graph import AgentState

def policy_node(state: AgentState) -> dict:
    result = check_policy(
        customer_message=state.customer_message,
        retrieved_docs=state.retrieved_docs,
        investigation_findings=state.investigation.findings if state.investigation else "None yet.",
    )

    return {
        "policy_check": result,
    }