from rag_pipeline import answer_question
query = "My laptop cannot connect to Wi-Fi. What troubleshooting steps should I follow?"
print("\n========== KNOWN QUESTION TEST ==========")
print("User:", query)
answer, sources = answer_question(query)
print("\nAssistant:")
print(answer)
print("\nSources:")
for source in sources:
    print("-", source)
print("\n========== TEST COMPLETED ==========")
