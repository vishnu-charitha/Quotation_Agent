import os
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


# =========================================================
# CONFIGURATION
# =========================================================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "quotation_documents"
)

EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


# =========================================================
# CREATE QDRANT CLIENT
# =========================================================

def get_qdrant_client():

    print("Connecting to Qdrant...")

    if not QDRANT_URL:
        raise ValueError(
            "QDRANT_URL is missing in the .env file"
        )

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=60
    )

    return client


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    query: str,
    limit: int = 3
) -> List[Dict[str, Any]]:

    print("\nRetrieving relevant documents...")

    print("\nGenerating query embedding...")

    query_vector = embedding_model.encode(
        query
    ).tolist()

    print(
        f"Query vector size: {len(query_vector)}"
    )

    client = get_qdrant_client()

    print("\nSearching Qdrant...")

    try:

        search_result = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True
        )

        points = search_result.points

    except AttributeError:

        points = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )

    results = []

    for point in points:

        payload = point.payload or {}

        content = (
            payload.get("content")
            or payload.get("text")
            or payload.get("page_content")
            or ""
        )

        metadata = payload.get(
            "metadata",
            {}
        )

        results.append(
            {
                "content": content,
                "metadata": metadata,
                "score": float(point.score)
            }
        )

    return results


# =========================================================
# GET RAG CONTEXT
# =========================================================

def get_rag_context(
    query: str,
    limit: int = 3
) -> str:

    results = retrieve_documents(
        query=query,
        limit=limit
    )

    if not results:
        return "No relevant information found."

    context_parts = []

    for index, result in enumerate(
        results,
        start=1
    ):

        content = result.get(
            "content",
            ""
        )

        score = result.get(
            "score",
            0
        )

        context_parts.append(
            f"""
DOCUMENT {index}

Similarity Score: {score}

Content:
{content}
"""
        )

    return "\n\n".join(
        context_parts
    )