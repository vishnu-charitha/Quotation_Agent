import os

from dotenv import load_dotenv

from langchain_qdrant import QdrantVectorStore

from backend.rag.embeddings import get_embeddings


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# QDRANT CONFIGURATION
# =========================================================

QDRANT_URL = os.getenv("QDRANT_URL")

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "quotation_documents"


# =========================================================
# CREATE VECTOR STORE
# =========================================================

def create_vector_store(documents):

    print("\nInitializing Embedding Model...")

    embeddings = get_embeddings()


    print("\nCreating Qdrant Vector Store...")


    vector_store = QdrantVectorStore.from_documents(

        documents=documents,

        embedding=embeddings,

        url=QDRANT_URL,

        api_key=QDRANT_API_KEY,

        collection_name=COLLECTION_NAME,

        # Recreates collection if embedding dimensions changed
        force_recreate=True
    )


    print(
        f"\nSuccessfully stored "
        f"{len(documents)} chunks in Qdrant."
    )


    return vector_store


# =========================================================
# LOAD EXISTING VECTOR STORE
# =========================================================

def get_vector_store():

    print("\nLoading Existing Qdrant Vector Store...")


    embeddings = get_embeddings()


    vector_store = QdrantVectorStore.from_existing_collection(

        embedding=embeddings,

        url=QDRANT_URL,

        api_key=QDRANT_API_KEY,

        collection_name=COLLECTION_NAME
    )


    return vector_store