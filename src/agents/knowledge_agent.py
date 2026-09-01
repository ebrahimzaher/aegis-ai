from rag import get_vector_store

def retrieve_knowledge(query: str, k: int = 3):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)

    return [doc.page_content for doc in results]

if __name__ == "__main__":
    docs = retrieve_knowledge("I was charged twice for my subscription")
    for i, doc in enumerate(docs, 1):
        print(f"--- Result {i} ---")
        print(doc)
        print()