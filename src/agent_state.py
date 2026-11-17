from langgraph.graph import MessagesState
class ITSupportState(MessagesState):
    pending_ticket_description: str | None
    awaiting_confirmation: bool
    last_grounded_result: str | None