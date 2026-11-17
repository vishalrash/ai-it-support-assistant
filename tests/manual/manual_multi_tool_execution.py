from langchain_ollama import ChatOllama
from langchain_tools import it_support_tools
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0
)
llm_with_tools = llm.bind_tools(it_support_tools)
user_query = """
My laptop cannot connect to the company VPN.
Also, check the current status of ticket TKT1002.
"""
print("\n========== MULTI-TOOL TEST ==========")
print("\nUser Request:")
print(user_query)
response = llm_with_tools.invoke(user_query)
tools_by_name = {
    tool.name: tool
    for tool in it_support_tools
}
if response.tool_calls:
    print("\nNumber of tools requested:", len(response.tool_calls))
    for index, tool_call in enumerate(response.tool_calls, start=1):
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print(f"\n========== TOOL {index} ==========")
        print("Tool Name:", tool_name)
        print("Arguments:", tool_args)
        selected_tool = tools_by_name.get(tool_name)
        if selected_tool is None:
            print("Unknown tool requested.")
            continue
        result = selected_tool.invoke(tool_args)
        print("\nExecution Result:")
        print(result)
else:
    print("\nNo tools were requested.")
print("\n========== MULTI-TOOL TEST COMPLETED ==========")