
from langchain_tools import knowledge_base_search

print("\n========== GROUNDED KNOWLEDGE TOOL TEST ==========")

result = knowledge_base_search.invoke({
    "query": "My laptop is running very slowly. What should I do?"
})

print("\nTool result:")
print(result)

print("\n========== TEST COMPLETED ==========")
