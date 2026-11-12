
from tools import search_knowledge_base


print("\n========== KNOWLEDGE BASE TOOL TEST ==========")

query = "How do I configure my company VPN?"

print("\nInput Query:")
print(query)

# Execute the tool
result = search_knowledge_base(query)

print("\nTool Output:")
print(result)

print("\n========== TEST COMPLETED ==========")
