from document_loader import load_documents
from text_splitter import split_documents
from embeddings import get_embedding_model
from vector_store import build_vector_store
documents = load_documents()
chunks = split_documents(documents)
embedding_model = get_embedding_model()
vector_store = build_vector_store(chunks, embedding_model)
query = "My laptop is running very slowly"
results = vector_store.similarity_search(query, k=3)
print("\n========== SEARCH RESULTS ==========")
for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Source:", result.metadata.get("source"))
    print("Content:")
    print(result.page_content)
print("\n========== TEST COMPLETED ==========")
