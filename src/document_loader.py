from pathlib import Path
import logging
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def load_documents(directory="knowledge_base"):
    """
    Load PDF, TXT and Markdown documents
    from the knowledge base directory.
    """
    knowledge_path = Path(directory)
    if not knowledge_path.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {directory}"
        )
    documents = []
    for file_path in sorted(knowledge_path.rglob("*")):
        if not file_path.is_file():
            continue
        extension = file_path.suffix.lower()
        try:
            if extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif extension in [".txt", ".md"]:
                loader = TextLoader(
                    str(file_path),
                    encoding="utf-8"
                )
            else:
                logger.warning(
                    f"Unsupported file skipped: {file_path.name}"
                )
                continue
            loaded_docs = loader.load()
            for document in loaded_docs:
                document.metadata["source"] = str(
                    file_path.relative_to(knowledge_path)
                )
            documents.extend(loaded_docs)
            logger.info(
                f"Loaded {file_path.name}: {len(loaded_docs)} document(s)"
            )
        except Exception as error:
            logger.exception(
                f"Failed to load {file_path.name}: {error}"
            )
    if not documents:
        raise ValueError("No documents were successfully loaded.")
    logger.info(f"Total loaded documents: {len(documents)}")
    return documents
