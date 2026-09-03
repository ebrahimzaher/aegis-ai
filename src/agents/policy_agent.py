from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import settings
from graph import PolicyOutput
from prompts import POLICY_SYSTEM_PROMPT

_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

_policy_llm = _llm.with_structured_output(PolicyOutput)

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", POLICY_SYSTEM_PROMPT),
        (
            "human",
            "Customer message: {customer_message}\n\n"
            "Retrieved policy excerpts:\n{policy_context}\n\n"
            "Investigation findings (if any): {investigation_findings}",
        ),
    ]
)

_policy_chain = _prompt | _policy_llm

def check_policy(customer_message: str, retrieved_docs: list[str], investigation_findings: str = "None yet.",) -> PolicyOutput:
    policy_context = "\n\n".join(retrieved_docs) if retrieved_docs else "None retrieved."

    return _policy_chain.invoke(
        {
            "customer_message": customer_message,
            "policy_context": policy_context,
            "investigation_findings": investigation_findings,
        }
    )

if __name__ == "__main__":
    sample_docs = [
        "Refunds under $100 can be auto-approved by the support agent. "
        "Refunds of $100 or more, or any refund requested after the "
        "14-day window, require manager approval before being issued."
    ]
    output = check_policy(
        customer_message="I was charged twice for my subscription, I want a refund.",
        retrieved_docs=sample_docs,
        investigation_findings="Duplicate charge confirmed on order ord_9001, amount $29.00.",
    )
    print(output)