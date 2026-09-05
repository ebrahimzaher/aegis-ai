import uuid
from fastapi import APIRouter, HTTPException
from langgraph.types import Command
from api import ApprovalRequest, TicketRequest, TicketResponse
from graph import AgentState
from graph import build_workflow

router = APIRouter()

_workflow = build_workflow()

def _extract_interrupt_payload(result: dict) -> dict:
    return result["__interrupt__"][0].value

@router.post("/tickets", response_model=TicketResponse)
def create_ticket(payload: TicketRequest):
    """Open a new support ticket and run it through the agent pipeline."""
    ticket_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": ticket_id}}

    initial_state = AgentState(
        ticket_id=ticket_id,
        customer_id=payload.customer_id,
        customer_message=payload.message,
    )

    result = _workflow.invoke(initial_state, config=config)

    if "__interrupt__" in result:
        return TicketResponse(
            ticket_id=ticket_id,
            status="pending_approval",
            pending_approval=_extract_interrupt_payload(result),
        )
    
    return TicketResponse(
        ticket_id=ticket_id,
        status="resolved",
        final_response=result["final_response"],
    )

@router.post("/tickets/{ticket_id}/approve", response_model=TicketResponse)
def approve_ticket(ticket_id: str, payload: ApprovalRequest):
    """Resume a ticket that's paused waiting for human approval."""
    config = {"configurable": {"thread_id": ticket_id}}

    state = _workflow.get_state(config)
    if not state.next:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found or not currently awaiting approval.",
        )

    result = _workflow.invoke(Command(resume=payload.approved), config=config)

    return TicketResponse(
        ticket_id=ticket_id,
        status="resolved",
        final_response=result["final_response"],
    )