from langchain_text_splitters import RecursiveCharacterTextSplitter
def split_documents(documents):
    """
    Divide loaded documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")
    return chunks
