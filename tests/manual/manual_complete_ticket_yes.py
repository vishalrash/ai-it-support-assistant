from langchain_core.messages import HumanMessage
from langgraph.types import Command
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "complete-ticket-yes-001"
    }
}
initial_state = {
    "messages": [
        HumanMessage(
            content=(
                "Create a support ticket. "
                "My office printer is not working."
            )
        )
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== COMPLETE TICKET YES TEST ==========")
paused_result = agent_graph.invoke(
    initial_state,
    config=config
)
if "__interrupt__" not in paused_result:
    print("ERROR: Approval was not requested.")
    raise SystemExit(1)
print("\nApproval requested:")
print(paused_result["__interrupt__"][0].value)
print("\nUser response: YES")
final_result = agent_graph.invoke(
    Command(resume="yes"),
    config=config
)
print("\nFinal result:")
for message in final_result["messages"]:
    print(message.content)
print("\nPending ticket:")
print(final_result.get("pending_ticket_description"))
print("\nAwaiting confirmation:")
print(final_result.get("awaiting_confirmation"))
print("\n========== TEST COMPLETED ==========")
