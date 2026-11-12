
from document_loader import load_documents
from text_splitter import split_documents
from embeddings import get_embedding_model
from vector_store import build_vector_store


def main():
    print("=" * 50)
    print("       IT SUPPORT KNOWLEDGE BASE INDEXING")
    print("=" * 50)

    # Step 1: Load documents
    print("\nStep 1: Loading knowledge-base documents...")
    documents = load_documents("knowledge_base")

    # Step 2: Split documents into chunks
    print("\nStep 2: Splitting documents into chunks...")
    chunks = split_documents(documents)

    # Step 3: Load embedding model
    print("\nStep 3: Loading embedding model...")
    embedding_model = get_embedding_model()

    # Step 4: Store chunks in ChromaDB
    print("\nStep 4: Building ChromaDB vector store...")
    build_vector_store(chunks, embedding_model)

    print("\nKnowledge base indexed successfully!")


if __name__ == "__main__":
    main()
