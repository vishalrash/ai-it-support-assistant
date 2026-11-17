from agent import agent_node
from tool_node import tool_execution_node
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
print("\n========== TOOL NODE TEST ==========")
agent_result = agent_node(state)
state["messages"].extend(agent_result["messages"])
tool_result = tool_execution_node(state)
for message in tool_result["messages"]:
    print("\nTool Result:")
    print(message.content)
print("\n========== TEST COMPLETED ==========")
