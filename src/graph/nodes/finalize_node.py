from graph import AgentState

def finalize_node(state: AgentState) -> dict:
    if state.requires_human_approval and not state.human_approved:
        final_response = (
            "Thanks for your patience — your request has been escalated to "
            "a support specialist for review and you'll hear back shortly."
        )
    elif state.requires_human_approval and state.human_approved:
        final_response = state.resolution.proposed_action
    else:
        final_response = state.resolution.proposed_action

    return {
        "final_response": final_response,
    }