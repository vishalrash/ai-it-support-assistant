from langchain_chroma import Chroma
def build_vector_store(chunks, embedding_model):
    collection_name = "it_support_knowledge"
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory="vector_store",
        embedding_function=embedding_model
    )
    existing_count = vector_store._collection.count()
    if existing_count > 0:
        vector_store.delete_collection()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="vector_store",
        collection_name=collection_name
    )
    print("Documents successfully stored in ChromaDB!")
    print("Total chunks stored:", vector_store._collection.count())
    return vector_store
