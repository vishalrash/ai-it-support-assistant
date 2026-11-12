from langchain_core.messages import AIMessage
from tool_node import tool_execution_node
fake_message = AIMessage(
    content="",
    tool_calls=[
        {
            "name": "request_support_ticket",
            "args": {
                "issue_description": (
                    "My office printer is not working."
                )
            },
            "id": "ticket-request-test-001",
            "type": "tool_call"
        }
    ]
)
state = {
    "messages": [fake_message],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== TICKET REQUEST NODE TEST ==========")
result = tool_execution_node(state)
print("\nTool response:")
for message in result["messages"]:
    print(message.content)
print("\nPending ticket:")
print(result.get("pending_ticket_description"))
print("\nAwaiting confirmation:")
print(result.get("awaiting_confirmation"))
print("\n========== TEST COMPLETED ==========")