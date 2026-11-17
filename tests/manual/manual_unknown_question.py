from rag_pipeline import answer_question
query = "What is my company's internal Wi-Fi password?"
print("\n========== UNKNOWN QUESTION TEST ==========")
print("User:", query)
answer, sources = answer_question(query)
print("\nAssistant:")
print(answer)
print("\nRetrieved Sources:")
for source in sources:
    print("-", source)
print("\n========== TEST COMPLETED ==========")
