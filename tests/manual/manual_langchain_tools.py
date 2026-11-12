
from langchain_tools import it_support_tools

print("\n========== LANGCHAIN TOOLS TEST ==========")

for tool in it_support_tools:

    print("\nTool Name:", tool.name)

    print("\nDescription:")
    print(tool.description)

    print("\nInput Schema:")
    print(tool.args)

    print("-" * 50)

print("\nTotal tools registered:", len(it_support_tools))

print("\n========== TEST COMPLETED ==========")
