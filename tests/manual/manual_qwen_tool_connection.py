from langchain_ollama import ChatOllama
from langchain_tools import it_support_tools
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)
llm_with_tools = llm.bind_tools(it_support_tools)
response = llm_with_tools.invoke(
    "Check the current status of ticket TKT1002."
)
print("\n========== QWEN3 TOOL CONNECTION TEST ==========")
print("\nModel response:")
print(response)
print("\nRequested tool calls:")
if response.tool_calls:
    for tool_call in response.tool_calls:
        print("Tool name:", tool_call["name"])
        print("Arguments:", tool_call["args"])
else:
    print("No tool call was generated.")
print("\n========== TEST COMPLETED ==========")