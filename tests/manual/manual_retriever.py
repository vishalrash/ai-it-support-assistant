from retriever import get_retriever
retriever = get_retriever()
query = "I forgot my company password. How can I reset it?"
results = retriever.invoke(query)
print("\n========== RETRIEVER TEST ==========")
print("User Question:", query)
print("Number of results:", len(results))
for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Source:", result.metadata.get("source"))
    print("Content:")
    print(result.page_content)
print("\n========== TEST COMPLETED ==========")