from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import settings
from graph import CriticOutput, InvestigationOutput, PolicyOutput, ResolutionOutput
from prompts import CRITIC_SYSTEM_PROMPT

_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

_critic_llm = _llm.with_structured_output(CriticOutput)
 
_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CRITIC_SYSTEM_PROMPT),
        (
            "human",
            "Customer message: {customer_message}\n\n"
            "Investigation findings:\n{investigation_context}\n\n"
            "Applicable policy:\n{policy_context}\n\n"
            "Proposed resolution:\n{resolution_context}",
        ),
    ]
)

_critic_chain = _prompt | _critic_llm

def critique(customer_message: str, investigation: InvestigationOutput, policy_check: PolicyOutput, resolution: ResolutionOutput,) -> CriticOutput:
    investigation_context = (
        f"findings: {investigation.findings}\n"
        f"relevant_order_id: {investigation.relevant_order_id}"
    )

    policy_context = (
        f"applicable_policy: {policy_check.applicable_policy}\n"
        f"requires_human_approval: {policy_check.requires_human_approval}\n"
        f"notes: {policy_check.notes}"
    )

    resolution_context = (
        f"proposed_action: {resolution.proposed_action}\n"
        f"is_sensitive_action: {resolution.is_sensitive_action}\n"
        f"reasoning: {resolution.reasoning}"
    )

    return _critic_chain.invoke(
        {
            "customer_message": customer_message,
            "investigation_context": investigation_context,
            "policy_context": policy_context,
            "resolution_context": resolution_context,
        }
    )

if __name__ == "__main__":
    sample_investigation = InvestigationOutput(
        findings="Duplicate charge confirmed on order ord_9001, amount $29.00.",
        relevant_order_id="ord_9001",
        data_sources_checked=["lookup_customer_orders"],
    )
    sample_policy = PolicyOutput(
        applicable_policy="Refunds under $100 can be auto-approved by the support agent.",
        requires_human_approval=False,
        notes="Amount ($29.00) is under the $100 auto-approval threshold.",
    )
    sample_resolution = ResolutionOutput(
        proposed_action="Issue a refund of $29.00 for the duplicate charge on order ord_9001.",
        is_sensitive_action=True,
        reasoning="Investigation confirmed a duplicate charge; policy allows auto-approval under $100.",
    )

    output = critique(
        customer_message="I was charged twice for my subscription, please help.",
        investigation=sample_investigation,
        policy_check=sample_policy,
        resolution=sample_resolution,
    )
    print(output)