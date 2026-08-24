from backend.rag.document_loader import load_all_documents
from backend.rag.text_splitter import split_documents
from backend.rag.vector_store import create_vector_store


# ==========================================
# RAG INGESTION PIPELINE
# ==========================================

def ingest_documents():

    print("\n========================================")
    print("STARTING RAG INGESTION PIPELINE")
    print("========================================")


    # --------------------------------------
    # STEP 1: LOAD DOCUMENTS
    # --------------------------------------

    documents = load_all_documents()


    if not documents:

        print("\nNo documents found.")

        return


    # --------------------------------------
    # STEP 2: SPLIT DOCUMENTS INTO CHUNKS
    # --------------------------------------

    chunks = split_documents(
        documents
    )


    if not chunks:

        print("\nNo chunks created.")

        return


    # --------------------------------------
    # STEP 3: STORE IN QDRANT
    # --------------------------------------

    create_vector_store(
        chunks
    )


    print("\n========================================")
    print("RAG INGESTION COMPLETED SUCCESSFULLY")
    print("========================================")

    print(
        f"\nTotal documents processed: "
        f"{len(documents)}"
    )

    print(
        f"Total chunks stored: "
        f"{len(chunks)}"
    )


# ==========================================
# RUN INGESTION
# ==========================================

if __name__ == "__main__":

    ingest_documents()