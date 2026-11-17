from agent import agent_node
state = {
    "messages": [
        {
            "role": "user",
            "content": "Check the current status of ticket TKT1002."
        }
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}
result = agent_node(state)
print("\n========== AGENT NODE TEST ==========")
for message in result["messages"]:
    print("AI Response:", message.content)
    print("Tool Calls:", message.tool_calls)
print("\n========== TEST COMPLETED ==========")
