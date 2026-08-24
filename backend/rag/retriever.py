from typing import List, Dict, Any

from backend.rag.vector_store import get_vector_store


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    query: str,
    limit: int = 3
) -> List[Dict[str, Any]]:

    print("\n==============================")
    print("RAG RETRIEVER")
    print("==============================")

    print(f"\nQuery:\n{query}")


    # -----------------------------------------------------
    # LOAD VECTOR STORE
    # -----------------------------------------------------

    vector_store = get_vector_store()


    print("\nSearching Qdrant Vector Database...")


    # -----------------------------------------------------
    # SIMILARITY SEARCH
    # -----------------------------------------------------

    documents = vector_store.similarity_search_with_score(
        query=query,
        k=limit
    )


    # -----------------------------------------------------
    # FORMAT RESULTS
    # -----------------------------------------------------

    results = []

    for document, score in documents:

        results.append(
            {
                "content": document.page_content,

                "metadata": document.metadata,

                "score": float(score)
            }
        )


    print(
        f"\nRetrieved {len(results)} relevant documents."
    )


    return results


# =========================================================
# GET RAG CONTEXT
# =========================================================

def get_rag_context(
    query: str,
    limit: int = 3
) -> str:

    print("\nCreating RAG Context...")


    # -----------------------------------------------------
    # RETRIEVE DOCUMENTS
    # -----------------------------------------------------

    results = retrieve_documents(
        query=query,
        limit=limit
    )


    # -----------------------------------------------------
    # CHECK RESULTS
    # -----------------------------------------------------

    if not results:

        return (
            "No relevant information found "
            "in the knowledge base."
        )


    # -----------------------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------------------

    context_parts = []


    for index, result in enumerate(
        results,
        start=1
    ):

        content = result.get(
            "content",
            ""
        )

        metadata = result.get(
            "metadata",
            {}
        )

        score = result.get(
            "score",
            0.0
        )


        context_parts.append(

            f"""
========================================
DOCUMENT {index}
========================================

Similarity Score:
{score}

Content:
{content}

Metadata:
{metadata}
"""
        )


    # -----------------------------------------------------
    # COMBINE CONTEXT
    # -----------------------------------------------------

    context = "\n\n".join(
        context_parts
    )


    print("\nRAG Context Created Successfully.")


    return context


# =========================================================
# TEST RETRIEVER
# =========================================================

if __name__ == "__main__":

    print("\n========================================")
    print("TESTING RAG RETRIEVER")
    print("========================================")


    test_query = (
        "Find laptops with Intel Core i5, "
        "16GB RAM and 512GB SSD"
    )


    context = get_rag_context(
        query=test_query,
        limit=3
    )


    print("\n========================================")
    print("RETRIEVED RAG CONTEXT")
    print("========================================")

    print(context)