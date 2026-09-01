from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import settings

@lru_cache
def get_embedding_function() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)

@lru_cache
def get_vector_store() -> Chroma:
    return Chroma(
        collection_name="faqs",
        embedding_function=get_embedding_function(),
        persist_directory=settings.chroma_persist_dir,
    )