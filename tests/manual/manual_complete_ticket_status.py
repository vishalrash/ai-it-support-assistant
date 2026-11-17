from langchain_core.messages import HumanMessage
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "complete-ticket-status-001"
    }
}
initial_state = {
    "messages": [
        HumanMessage(
            content="Check the status of ticket TKT1002."
        )
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== COMPLETE TICKET STATUS TEST ==========")
result = agent_graph.invoke(
    initial_state,
    config=config
)
print("\nAgent response:")
for message in result["messages"]:
    if message.content:
        print(message.content)
print("\n========== TEST COMPLETED ==========")
