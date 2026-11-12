from document_loader import load_documents
from text_splitter import split_documents
documents = load_documents()
chunks = split_documents(documents)
print("\n========== CHUNKING TEST ==========")
for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}")
    print("Source:", chunk.metadata["source"])
    print("Characters:", len(chunk.page_content))
    print("Content preview:")
    print(chunk.page_content[:150])
print("\n========== TEST COMPLETED ==========")
