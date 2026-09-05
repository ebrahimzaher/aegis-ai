import uuid
from enum import Enum
from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator

def _coerce_bool(value):
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return value

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

class InvestigationOutput(BaseModel):
    findings: str = Field(description="What was found in the customer's order/account data")
    relevant_order_id: Optional[str] = None
    data_sources_checked: list[str] = Field(default_factory=list)

class PolicyOutput(BaseModel):
    applicable_policy: str = Field(description="The relevant policy rule for this case, in plain language")
    requires_human_approval: Union[bool, str] = Field(
        description="True if company policy requires a human/manager to approve the action"
    )
    notes: str = ""

    @field_validator("requires_human_approval", mode="before")
    @classmethod
    def coerce_requires_human_approval(cls, v):
        return _coerce_bool(v)

    def model_post_init(self, __context):
        self.requires_human_approval = bool(self.requires_human_approval)

class ResolutionOutput(BaseModel):
    proposed_action: str = Field(description="The concrete action/response proposed for the customer")
    is_sensitive_action: Union[bool, str] = Field(
        description="True if this action is a refund, cancellation, or other irreversible change"
    )
    reasoning: str = Field(description="Why this action was chosen, referencing findings/policy")

    @field_validator("is_sensitive_action", mode="before")
    @classmethod
    def coerce_is_sensitive_action(cls, v):
        return _coerce_bool(v)

    def model_post_init(self, __context):
        self.is_sensitive_action = bool(self.is_sensitive_action)

class CriticOutput(BaseModel):
    score: float = Field(ge=0, le=10, description="Quality score out of 10 for the proposed resolution")
    is_hallucination_risk: Union[bool, str] = Field(
        description="True if the proposed action is not fully supported by the findings/policy given"
    )
    feedback: str = Field(description="Brief explanation of the score, and what to fix if score is low")

    @field_validator("is_hallucination_risk", mode="before")
    @classmethod
    def coerce_is_hallucination_risk(cls, v):
        return _coerce_bool(v)

    def model_post_init(self, __context):
        self.is_hallucination_risk = bool(self.is_hallucination_risk)

class AgentState(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ticket_id: str
    customer_id: Optional[str] = None
    customer_message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    intent: Optional[Intent] = None
    priority: Optional[Priority] = None

    retrieved_docs: list[str] = Field(default_factory=list)

    investigation: Optional[InvestigationOutput] = None

    policy_check: Optional[PolicyOutput] = None

    resolution: Optional[ResolutionOutput] = None

    critic: Optional[CriticOutput] = None

    requires_human_approval: bool = False
    human_approved: Optional[bool] = None

    final_response: Optional[str] = None
    retry_count: int = 0