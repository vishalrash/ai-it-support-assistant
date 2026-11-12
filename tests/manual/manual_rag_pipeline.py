from rag_pipeline import answer_question
query = "I forgot my company password. How can I reset it?"
print("\n========== AI IT SUPPORT ASSISTANT ==========")
print("User:", query)
answer, sources = answer_question(query)
print("\nAssistant:")
print(answer)
print("\nSources:")
for source in sources:
    print("-", source)
print("\n========== TEST COMPLETED ==========")