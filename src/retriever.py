from langchain_chroma import Chroma
try:
    from .embeddings import get_embedding_model
except ImportError:
    from embeddings import get_embedding_model
def get_retriever():
    """
    Load the existing ChromaDB database
    and return a retriever.
    """
    embedding_model = get_embedding_model()
    vector_store = Chroma(
        collection_name="it_support_knowledge",
        persist_directory="vector_store",
        embedding_function=embedding_model
    )
    print("ChromaDB connected successfully!")
    print("Stored chunks:", vector_store._collection.count())
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    return retriever
