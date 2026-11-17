from agent_graph import agent_graph
initial_state = {
    "messages": [
        {
            "role": "user",
            "content": (
                "My laptop is running very slowly. "
                "What should I do to fix it?"
            )
        }
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
print("\n========== KNOWLEDGE BASE AGENT TEST ==========")
result = agent_graph.invoke(initial_state)
print("\nAI Support Assistant:")
print(result["messages"][-1].content)
print("\n========== SOURCES USED ==========")
for message in result["messages"]:
    if getattr(message, "type", None) == "tool":
        print(message.content[:1000])
print("\n========== TEST COMPLETED ==========")
