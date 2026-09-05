from agents import critique
from config import settings
from graph import AgentState

def critic_node(state: AgentState) -> dict:
    result = critique(
        customer_message=state.customer_message,
        investigation=state.investigation,
        policy_check=state.policy_check,
        resolution=state.resolution,
    )

    needs_approval = (
        state.policy_check.requires_human_approval
        or state.resolution.is_sensitive_action
        or result.is_hallucination_risk
        or result.score < settings.critic_score_threshold
    )

    return {
        "critic": result,
        "requires_human_approval": needs_approval,
    }