
from agent_graph import agent_graph

initial_state = {
    "messages": [
        {
            "role": "user",
            "content": "Check the current status of ticket TKT1002."
        }
    ],
    "pending_ticket_description": None,
    "awaiting_confirmation": False
}

print("\n========== COMPLETE AGENT GRAPH TEST ==========")

result = agent_graph.invoke(initial_state)

print("\nFinal AI Response:")

print(result["messages"][-1].content)

print("\n========== TEST COMPLETED ==========")
