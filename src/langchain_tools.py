from langchain_core.tools import tool
from tools import (
    get_ticket_status,
    create_support_ticket
)

from rag_pipeline import answer_question
@tool
def knowledge_base_search(query: str) -> str:
    """
    Search the internal IT knowledge base and return
    a grounded answer with its source documents.
    """
    answer, sources = answer_question(query)

    source_text = ", ".join(sources) if sources else "No sources found"

    return (
        f"Grounded IT Support Answer:\n{answer}\n\n"
        f"Sources: {source_text}"
    )
@tool
def ticket_status_lookup(ticket_id: str) -> str:
    """
    Retrieve the status and details of an existing
    IT support ticket.
    """
    return get_ticket_status(ticket_id)
@tool
def request_support_ticket(issue_description: str) -> str:
    """
    Request creation of a new IT support ticket.

    This tool only prepares the ticket request.
    The application must obtain explicit user approval
    before actually creating and saving the ticket.
    """
    return (
        "TICKET_REQUESTED: "
        + issue_description.strip()
    )
def create_approved_ticket(issue_description: str) -> str:
    return create_support_ticket(issue_description)
it_support_tools = [
    knowledge_base_search,
    ticket_status_lookup,
    request_support_ticket
]