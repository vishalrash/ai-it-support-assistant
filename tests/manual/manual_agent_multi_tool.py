from langchain_core.messages import HumanMessage, AIMessage

from agent_graph import agent_graph

config = {
    "configurable": {
        "thread_id": "multi-tool-test"
    }
}

question = (
    "My company VPN is not connecting. "
    "Please help me troubleshoot it. "
    "Also, check the status of ticket TKT1002."
)

result = agent_graph.invoke(
    {
        "messages": [
            HumanMessage(content=question)
        ]
    },
    config=config
)

print("\n========== MULTI-TOOL TEST ==========")

print("\nFINAL AGENT RESPONSE:")

for message in reversed(result["messages"]):
    if isinstance(message, AIMessage) and message.content:
        print(message.content)
        break

print("\n========== TEST COMPLETED ==========")