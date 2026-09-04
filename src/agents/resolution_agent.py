from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import settings
from graph import InvestigationOutput, PolicyOutput, ResolutionOutput
from prompts import RESOLUTION_SYSTEM_PROMPT

_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

_resolution_llm = _llm.with_structured_output(ResolutionOutput)

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", RESOLUTION_SYSTEM_PROMPT),
        (
            "human",
            "Customer message: {customer_message}\n\n"
            "Relevant documentation:\n{knowledge_context}\n\n"
            "Investigation findings:\n{investigation_context}\n\n"
            "Applicable policy:\n{policy_context}",
        ),
    ]
)

_resolution_chain = _prompt | _resolution_llm

def resolve(customer_message: str, retrieved_docs: list[str], investigation: InvestigationOutput, policy_check: PolicyOutput,) -> ResolutionOutput:
    knowledge_context = "\n\n".join(retrieved_docs) if retrieved_docs else "None retrieved."

    investigation_context = (
        f"findings: {investigation.findings}\n"
        f"relevant_order_id: {investigation.relevant_order_id}\n"
        f"data_sources_checked: {investigation.data_sources_checked}"
    )

    policy_context = (
        f"applicable_policy: {policy_check.applicable_policy}\n"
        f"requires_human_approval: {policy_check.requires_human_approval}\n"
        f"notes: {policy_check.notes}"
    )

    return _resolution_chain.invoke(
        {
            "customer_message": customer_message,
            "knowledge_context": knowledge_context,
            "investigation_context": investigation_context,
            "policy_context": policy_context,
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
    sample_docs = [
        "Duplicate charges are automatically refunded within 5-7 business days."
    ]

    output = resolve(
        customer_message="I was charged twice for my subscription, please help.",
        retrieved_docs=sample_docs,
        investigation=sample_investigation,
        policy_check=sample_policy,
    )
    print(output)