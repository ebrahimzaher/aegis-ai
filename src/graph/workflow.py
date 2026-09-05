from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.types import Command
from graph.nodes import triage_node, knowledge_node, investigation_node, policy_node, resolution_node, critic_node, human_approval_node, finalize_node
from graph import AgentState

def _route_after_critic(state: AgentState) -> str:
    return "human_approval" if state.requires_human_approval else "finalize"

def build_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("triage", triage_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("investigation", investigation_node)
    graph.add_node("policy", policy_node)
    graph.add_node("resolution", resolution_node)
    graph.add_node("critic", critic_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("finalize", finalize_node)

    graph.set_entry_point("triage")

    graph.add_edge("triage", "knowledge")
    graph.add_edge("triage", "investigation")

    graph.add_edge("knowledge", "policy")
    graph.add_edge("investigation", "policy")

    graph.add_edge("policy", "resolution")
    graph.add_edge("resolution", "critic")

    graph.add_conditional_edges(
        "critic",
        _route_after_critic,
        {"human_approval": "human_approval", "finalize": "finalize"},
    )
    graph.add_edge("human_approval", "finalize")
    graph.add_edge("finalize", END)

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)
 
 
if __name__ == "__main__":
    app = build_workflow()
    config = {"configurable": {"thread_id": "ticket-001"}}

    initial_state = AgentState(
        ticket_id="ticket-001",
        customer_id="cust_001",
        customer_message="I was charged twice for my subscription this month, please help.",
    )

    result = app.invoke(initial_state, config=config)

    if "__interrupt__" in result:
        payload = result["__interrupt__"][0].value
        print("--- PAUSED: HUMAN APPROVAL NEEDED ---")
        print(payload)

        answer = input("\nApprove this action? (y/n): ").strip().lower()
        result = app.invoke(Command(resume=(answer == "y")), config=config)

    print("\n--- FINAL STATE ---")
    for key, value in result.items():
        print(f"{key}: {value}")