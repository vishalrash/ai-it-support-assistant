from langchain_ollama import ChatOllama
from langchain_tools import it_support_tools
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)
llm_with_tools = llm.bind_tools(it_support_tools)
user_query = "Check the current status of ticket TKT1002."
response = llm_with_tools.invoke(user_query)
tools_by_name = {
    tool.name: tool
    for tool in it_support_tools
}
print("\n========== TOOL EXECUTION TEST ==========")
if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print("\nSelected Tool:", tool_name)
        print("Arguments:", tool_args)
        selected_tool = tools_by_name.get(tool_name)
        if selected_tool is None:
            print("Error: Unknown tool requested.")
            continue
        result = selected_tool.invoke(tool_args)
        print("\nTool Execution Result:")
        print(result)
else:
    print("The model did not request a tool.")
print("\n========== TEST COMPLETED ==========")