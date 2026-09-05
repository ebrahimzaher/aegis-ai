from langgraph.types import interrupt
from graph import AgentState

def human_approval_node(state: AgentState) -> dict:
    """Pause and wait for a human decision on the proposed resolution."""
    decision = interrupt(
        {
            "reason": "This ticket requires human approval before the resolution is finalized.",
            "proposed_action": state.resolution.proposed_action,
            "is_sensitive_action": state.resolution.is_sensitive_action,
            "critic_score": state.critic.score,
            "critic_feedback": state.critic.feedback,
        }
    )

    approved = bool(decision)

    return {
        "human_approved": approved,
    }