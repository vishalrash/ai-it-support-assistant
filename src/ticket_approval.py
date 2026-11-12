from langgraph.types import interrupt
from langchain_tools import create_approved_ticket
def ticket_approval_node(state):
    """
    Pause the workflow until the user approves
    or rejects ticket creation.
    """
    issue = state["pending_ticket_description"]
    while True:
        approval = interrupt({
            "question": "Do you approve creating this support ticket?",
            "issue_description": issue,
            "options": ["YES", "NO"]
        })
        if isinstance(approval, str):
            response = approval.strip().lower()
        else:
            response = ""
        if response in ["yes", "y"]:
            result = create_approved_ticket(issue)
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": result
                    }
                ],
                "pending_ticket_description": None,
                "awaiting_confirmation": False
            }
        elif response in ["no", "n"]:
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "Ticket creation cancelled. No ticket was created."
                    }
                ],
                "pending_ticket_description": None,
                "awaiting_confirmation": False
            }
        else:
            print("Invalid response. Asking for confirmation again.")