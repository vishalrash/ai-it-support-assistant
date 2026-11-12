
from rag_pipeline import answer_question

question = (
    "My laptop is running very slowly. "
    "What troubleshooting steps should I follow?"
)

answer, sources = answer_question(question)

print("\n========== RAG ANSWER ==========")
print(answer)

print("\n========== SOURCES ==========")

for source in sources:
    print(source)
