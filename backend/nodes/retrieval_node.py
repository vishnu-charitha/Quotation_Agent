from backend.rag.retriever import retrieve_documents


def retrieval_node(state):

    print("\n==============================")
    print("RAG RETRIEVAL NODE")
    print("==============================")

    query = state.get("query", "")


    if not query:

        return {
            "rag_context": "",
            "retrieved_documents": []
        }


    # ------------------------------------------
    # RETRIEVE DOCUMENTS
    # ------------------------------------------

    retrieved_documents = retrieve_documents(
        query=query,
        limit=3
    )


    # ------------------------------------------
    # BUILD RAG CONTEXT
    # ------------------------------------------

    context_parts = []


    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        context_parts.append(
            f"""
========================================
DOCUMENT {index}
========================================

Content:
{document["content"]}

Metadata:
{document["metadata"]}
"""
        )


    rag_context = "\n".join(
        context_parts
    )


    print("\nRAG Context Created Successfully.")

    print(
        f"Documents Retrieved: "
        f"{len(retrieved_documents)}"
    )


    return {

        "rag_context":
            rag_context,

        "retrieved_documents":
            retrieved_documents
    }