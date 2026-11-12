
from langchain_core.messages import HumanMessage, AIMessage
from agent_graph import agent_graph

config = {
    "configurable": {
        "thread_id": "grounded-agent-test-001"
    }
}

initial_state = {
    "messages": [
        HumanMessage(
            content=(
                "My laptop is running very slowly. "
                "What should I do?"
            )
        )
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}

print("\n========== COMPLETE AGENT TEST ==========")

result = agent_graph.invoke(
    initial_state,
    config=config
)

print("\n========== FINAL AGENT RESPONSE ==========")

for message in reversed(result["messages"]):
    if isinstance(message, AIMessage) and message.content:
        print(message.content)
        break

print("\n========== TEST COMPLETED ==========")
