from document_loader import load_documents
documents = load_documents()
print("\n========== DOCUMENT LOADING TEST ==========")
print("Total documents loaded:", len(documents))
for index, document in enumerate(documents, start=1):
    print(f"\nDocument {index}")
    print("Source:", document.metadata["source"])
    print("Content preview:")
    print(document.page_content[:200])
print("\n========== TEST COMPLETED ==========")