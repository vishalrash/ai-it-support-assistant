from langchain_core.messages import HumanMessage, AIMessage
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "wifi-question-test"
    }
}
question = "My laptop cannot connect to the company Wi-Fi. How can I troubleshoot it?"
result = agent_graph.invoke(
    {
        "messages": [
            HumanMessage(content=question)
        ]
    },
    config=config
)
print("\n========== WI-FI TROUBLESHOOTING TEST ==========")
for message in reversed(result["messages"]):
    if isinstance(message, AIMessage) and message.content:
        print("\nFINAL AGENT RESPONSE:")
        print(message.content)
        break
print("\n========== TEST COMPLETED ==========")