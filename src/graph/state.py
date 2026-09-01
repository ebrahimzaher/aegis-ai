import uuid
from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
 
class Intent(str, Enum):
    BILLING = "billing"
    REFUND = "refund"
    TECHNICAL_ISSUE = "technical_issue"
    ACCOUNT = "account"
    GENERAL_QUESTION = "general_question"
    OTHER = "other"

class TriageOutput(BaseModel):
    intent: Intent
    priority: Priority
    summary: str = Field(description="One-line summary of what the customer needs")

class AgentState(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticket_id: str
    customer_id: Optional[str] = None
    customer_message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    intent: Optional[Intent] = None
    priority: Optional[Priority] = None

    retrieved_docs: list[str] = Field(default_factory=list)
