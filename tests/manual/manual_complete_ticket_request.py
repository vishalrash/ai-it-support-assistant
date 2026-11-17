from langchain_core.messages import HumanMessage
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "complete-ticket-test-001"
    }
}
initial_state = {
    "messages": [
        HumanMessage(
            content=(
                "Please create a support ticket. "
                "My office printer is not working."
            )
        )
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== COMPLETE TICKET REQUEST TEST ==========")
result = agent_graph.invoke(
    initial_state,
    config=config
)
print("\nWorkflow result:")
if "__interrupt__" in result:
    print("\nApproval requested:")
    print(result["__interrupt__"][0].value)
    print("\nPending ticket:")
    print(result.get("pending_ticket_description"))
    print("\nAwaiting confirmation:")
    print(result.get("awaiting_confirmation"))
    print("\nWorkflow successfully paused for approval.")
else:
    print("\nWorkflow completed without an approval interrupt.")
    for message in result["messages"]:
        print(message.content)
print("\n========== TEST COMPLETED ==========")
