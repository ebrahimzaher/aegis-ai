from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
from rag import get_vector_store

FAQ_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "faqs"

def ingest_faqs() -> None:
    if not FAQ_DIR.exists():
        raise FileNotFoundError(
            f"FAQ folder not found at {FAQ_DIR}. Create it and add .md files first."
        )
 
    loader = DirectoryLoader(
        str(FAQ_DIR),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)
 
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
 
    print(
        f"Ingested {len(chunks)} chunks from {len(docs)} files "
        f"into {settings.chroma_persist_dir}"
    )

if __name__ == "__main__":
    ingest_faqs()