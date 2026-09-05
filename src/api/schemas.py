from typing import Optional
from pydantic import BaseModel, Field

class TicketRequest(BaseModel):
    customer_id: Optional[str] = None
    message: str = Field(..., min_length=1, description="The customer's message/complaint")

class TicketResponse(BaseModel):
    ticket_id: str
    status: str
    final_response: Optional[str] = None
    pending_approval: Optional[dict] = None

class ApprovalRequest(BaseModel):
    approved: bool