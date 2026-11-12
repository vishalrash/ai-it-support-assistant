import json
from pathlib import Path
from datetime import datetime
import uuid
from retriever import get_retriever
knowledge_retriever = get_retriever()
def search_knowledge_base(query: str) -> str:
    """
    Search the internal IT knowledge base
    and return relevant document information.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty.")
    try:
        results = knowledge_retriever.invoke(query)
        if not results:
            return "No relevant information found in the knowledge base."
        output = []
        for index, document in enumerate(results, start=1):
            source = document.metadata.get(
                "source", "Unknown source"
            )
            output.append(
                f"Result {index}\n"
                f"Source: {source}\n"
                f"Content:\n{document.page_content}"
            )
        return "\n\n".join(output)
    except ValueError:
        raise
    except Exception as error:
        raise RuntimeError(
            f"Knowledge base search failed: {error}"
        ) from error

def get_ticket_status(ticket_id: str) -> str:
    """
    Retrieve ticket details using its ticket ID.
    """
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")
    ticket_id = ticket_id.strip().upper()
    ticket_file = Path("data/tickets.json")
    if not ticket_file.exists():
        raise FileNotFoundError("Ticket database not found.")
    try:
        with ticket_file.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
        for ticket in tickets:
            if ticket["ticket_id"].upper() == ticket_id:
                return (
                    f"Ticket ID: {ticket['ticket_id']}\n"
                    f"Issue: {ticket['issue_description']}\n"
                    f"Status: {ticket['status']}\n"
                    f"Priority: {ticket['priority']}\n"
                    f"Created At: {ticket['created_at']}"
                )
        return f"No ticket found with ID: {ticket_id}"
    except json.JSONDecodeError as error:
        raise RuntimeError("Ticket database contains invalid JSON.") from error
    except (KeyError, TypeError) as error:
        raise RuntimeError("Ticket record has an invalid structure.") from error

def create_support_ticket(issue_description: str) -> str:
    """
    Create a new support ticket and save it to JSON.
    """
    if not isinstance(issue_description, str) or not issue_description.strip():
        raise ValueError("Issue description cannot be empty.")
    issue_description = issue_description.strip()
    ticket_file = Path("data/tickets.json")
    ticket_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        if ticket_file.exists():
            with ticket_file.open("r", encoding="utf-8") as file:
                tickets = json.load(file)
        else:
            tickets = []
        if not isinstance(tickets, list):
            raise RuntimeError("Ticket database must contain a JSON list.")
        existing_ids = {
            ticket.get("ticket_id")
            for ticket in tickets
            if isinstance(ticket, dict)
        }
        while True:
            ticket_id = f"TKT{uuid.uuid4().hex[:8].upper()}"
            if ticket_id not in existing_ids:
                break
        new_ticket = {
            "ticket_id": ticket_id,
            "employee_name": "Not provided",
            "issue_description": issue_description,
            "status": "Open",
            "priority": "Medium",
            "created_at": datetime.now().astimezone().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
        tickets.append(new_ticket)
        with ticket_file.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)
        return (
            "Support ticket created successfully!\n"
            f"Ticket ID: {ticket_id}\n"
            f"Issue: {issue_description}\n"
            "Status: Open\n"
            "Priority: Medium"
        )
    except json.JSONDecodeError as error:
        raise RuntimeError("Ticket database contains invalid JSON.") from error