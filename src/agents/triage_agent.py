import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config import settings
from graph import  TriageOutput
from prompts import TRIAGE_SYSTEM_PROMPT

_llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.llm_model,
    temperature=settings.llm_temperature,
)

_triage_llm = _llm.with_structured_output(TriageOutput)

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", TRIAGE_SYSTEM_PROMPT),
        ("human", "{customer_message}"),
    ]
)

_triage_chain = _prompt | _triage_llm

def triage_agent(customer_message: str) -> TriageOutput:
    return _triage_chain.invoke({"customer_message": customer_message})

if __name__ == "__main__":
    result = triage_agent(
        "I was charged twice for my subscription this month, please help."
    )
    print(result)