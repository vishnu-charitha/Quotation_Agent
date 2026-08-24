from backend.rag.retriever import retrieve_documents


def rag_retrieval_node(state):

    print("\n==============================")
    print("RAG RETRIEVAL NODE")
    print("==============================")

    query = state["query"]

    print("\nRetrieving relevant documents...")

    documents = retrieve_documents(
        query=query,
        limit=9
    )

    print(
        f"\nRetrieved {len(documents)} documents."
    )

    return {

        "retrieved_documents":
            documents

    }