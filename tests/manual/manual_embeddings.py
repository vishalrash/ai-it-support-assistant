from embeddings import get_embedding_model
embedding_model = get_embedding_model()
sentences = [
    "My laptop is running slowly.",
    "My computer performance is poor.",
    "How do I reset my company password?"
]
vectors = embedding_model.embed_documents(sentences)
print("\n========== EMBEDDING TEST ==========")
print("Number of sentences:", len(sentences))
for index, vector in enumerate(vectors):
    print(f"\nSentence {index + 1}: {sentences[index]}")
    print("Vector dimensions:", len(vector))
    print("First 10 vector values:", vector[:10])
print("\n========== TEST COMPLETED ==========")