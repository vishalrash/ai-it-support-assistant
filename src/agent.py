from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from agent_state import ITSupportState
from langchain_tools import it_support_tools
SYSTEM_PROMPT = """
You are an AI-powered internal IT Support Assistant.

You have access to these tools:
1. knowledge_base_search(query)
2. ticket_status_lookup(ticket_id)
3. request_support_ticket(issue_description)

TOOL SELECTION RULES:

1. For IT troubleshooting questions, always use
   knowledge_base_search before answering.

2. For questions about an existing ticket, use
   ticket_status_lookup.

3. Only use request_support_ticket when the user
   explicitly asks to create or raise a support ticket.


ANSWERING RULES:

1. Answer using ONLY information returned by the tools.
2. Never add troubleshooting steps from your own knowledge.
3. Never invent commands, keyboard shortcuts, URLs,
   settings, policies, credentials, or procedures.
4. Do not assume information that is not in the results.
5. If the retrieved information does not answer the
   question, say:

   "I couldn't find this information in the available
   IT knowledge base. Please contact your IT support team."

6. Explain the relevant steps clearly and in order.
7. Include the source filename only when knowledge_base_search was used.
8. Never invent a source filename.
9. For ticket-only responses, do not mention a document source.
10. Do not copy the entire raw tool output into your answer.
11. Do not claim that an action was completed unless
    the relevant tool confirms it.
12. For follow-up questions, use only information explicitly
    present in previous tool results or conversation context
    that originated from tool results.
13. Do not invent reasons, benefits, explanations, or
    additional troubleshooting advice.
14. When summarizing previous troubleshooting steps,
    preserve their original meaning without adding assumptions.

TICKET SAFETY:

1. Never create a ticket directly.
2. Use request_support_ticket to prepare a request.
3. The application will ask the user for approval.
4. A ticket is created only after explicit approval.
5. Never claim a ticket was created before approval.

If the user asks multiple independent questions,
use all the relevant tools.
"""


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    num_predict=500
)
llm_with_tools = llm.bind_tools(it_support_tools)
def agent_node(state: ITSupportState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    grounded_result = state.get("last_grounded_result")

    # Get the latest user message.
    latest_user_message = next(
        (
            message.content
            for message in reversed(state["messages"])
            if message.type == "human"
        ),
        ""
    )

    query = latest_user_message.lower().strip()

    # Handle source-document follow-up questions.
    if grounded_result and any(
        phrase in query
        for phrase in [
            "what was the source",
            "which source",
            "source document",
            "which document",
            "document name"
        ]
    ):

        import re

        sources = re.findall(
            r"Source(?:s)?(?: filename)?:\s*([^\n]+)",
            grounded_result,
            re.IGNORECASE
        )

        if sources:
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": (
                            "Source document: "
                            + sources[-1].strip()
                        )
                    }
                ]
            }

    # Handle summary follow-up questions.
    if grounded_result and any(
        phrase in query
        for phrase in [
            "summarize the solution",
            "summarize your solution",
            "summarize the steps",
            "summary of the solution",
            "summarize what you said",
            "repeat the solution"
        ]
    ):

        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": grounded_result
                }
            ]
        }

    # Normal agent processing for all other questions.
    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }