from langchain_core.messages import HumanMessage, AIMessage
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "complete-knowledge-test-002"
    }
}
initial_state = {
    "messages": [
        HumanMessage(
            content=(
                "My laptop is running very slowly. "
                "What troubleshooting steps should I follow?"
            )
        )
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== KNOWLEDGE SEARCH TEST ==========")
result = agent_graph.invoke(
    initial_state,
    config=config
)
print("\n========== FINAL AGENT ANSWER ==========")
for message in reversed(result["messages"]):
    if isinstance(message, AIMessage) and message.content:
        print(message.content)
        break
print("\n========== TEST COMPLETED ==========")
