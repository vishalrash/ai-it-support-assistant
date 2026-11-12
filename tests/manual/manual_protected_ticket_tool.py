from langchain_tools import (
    it_support_tools,
    create_approved_ticket
)
print("\n========== PROTECTED TOOL TEST ==========")
print("\nTools available to Qwen3:")
for tool in it_support_tools:
    print("-", tool.name)
print("\nProtected ticket creation function:")
print(create_approved_ticket.__name__)
print("\nNumber of AI-callable tools:", len(it_support_tools))
print("\n========== TEST COMPLETED ==========")