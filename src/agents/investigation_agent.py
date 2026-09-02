from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from config import settings
from graph.state import InvestigationOutput
from prompts.investigation_prompt import INVESTIGATION_SYSTEM_PROMPT
from tools.order_lookup import lookup_customer_orders

_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

_tools = [lookup_customer_orders]
_llm_with_tools = _llm.bind_tools(_tools)
_tool_by_name = {t.name: t for t in _tools}

def investigate(customer_message: str, customer_id: str) -> InvestigationOutput:
    messages = [
        SystemMessage(content=INVESTIGATION_SYSTEM_PROMPT),
        HumanMessage(
            content=f"customer_id: {customer_id}\ncustomer message: {customer_message}"
        ),
    ]

    ai_response = _llm_with_tools.invoke(messages)
    messages.append(ai_response)

    data_sources_checked = []

    for tool_call in ai_response.tool_calls:
        tool_fn = _tool_by_name[tool_call["name"]]
        tool_result = tool_fn.invoke(tool_call["args"])
        data_sources_checked.append(tool_call["name"])
        messages.append(
            ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
        )

    structured_llm = _llm.with_structured_output(InvestigationOutput)
    result: InvestigationOutput = structured_llm.invoke(messages)

    return InvestigationOutput(
        findings=getattr(result, "findings", "No findings returned."),
        relevant_order_id=getattr(result, "relevant_order_id", None),
        data_sources_checked=data_sources_checked
        or getattr(result, "data_sources_checked", []),
    )

if __name__ == "__main__":
    output = investigate(
        customer_message="I was charged twice for my subscription this month, please help.",
        customer_id="cust_001",
    )
    print(output)