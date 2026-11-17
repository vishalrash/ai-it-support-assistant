from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent_graph import agent_graph
config = {
    "configurable": {
        "thread_id": "unknown-question-test"
    }
}
question = "What is my company's internal Wi-Fi password?"
result = agent_graph.invoke(
    {
        "messages": [
            HumanMessage(content=question)
        ]
    },
    config=config
)
print("\n========== UNKNOWN QUESTION TEST ==========")
for message in reversed(result["messages"]):
    if isinstance(message, AIMessage) and message.content:
        print("\nFINAL AGENT RESPONSE:")
        print(message.content)
        break
print("\n========== TEST COMPLETED ==========")