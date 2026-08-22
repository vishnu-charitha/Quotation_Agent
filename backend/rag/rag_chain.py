import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from qdrant_client import QdrantClient


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_PATH = BASE_DIR / ".env"


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv(ENV_PATH)

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

COLLECTION_NAME = "quotation_documents"


# ==========================================
# VALIDATE ENV VARIABLES
# ==========================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing in .env file"
    )

if not QDRANT_URL:
    raise ValueError(
        "QDRANT_URL is missing in .env file"
    )

if not QDRANT_API_KEY:
    raise ValueError(
        "QDRANT_API_KEY is missing in .env file"
    )


print("Gemini API key loaded successfully.")


# ==========================================
# EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# CONNECT TO QDRANT
# ==========================================

def get_qdrant_client():

    print("\nConnecting to Qdrant...")

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=60
    )

    return client


# ==========================================
# RETRIEVE RELEVANT DOCUMENTS
# ==========================================

def retrieve_documents(query, limit=3):

    client = get_qdrant_client()

    print("Generating query embedding...")

    query_vector = embeddings.embed_query(query)

    print(
        f"Query vector size: {len(query_vector)}"
    )

    print("Searching Qdrant...")

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    documents = []

    for point in results.points:

        payload = point.payload

        content = payload.get(
            "page_content",
            ""
        )

        documents.append(
            {
                "content": content,
                "score": point.score
            }
        )

    return documents


# ==========================================
# CREATE GEMINI MODEL
# ==========================================

def get_llm():

    print("\nInitializing Gemini...")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    return llm


# ==========================================
# BUILD RAG CONTEXT
# ==========================================

def build_context(documents):

    context = ""

    for index, document in enumerate(
        documents,
        start=1
    ):

        context += f"""

DOCUMENT {index}

{document["content"]}

"""

    return context


# ==========================================
# MAIN RAG CHAIN
# ==========================================

def rag_chain(query):

    print("\n=================================")
    print("RAG CHAIN STARTED")
    print("=================================")

    print(f"\nUser Question:\n{query}")

    # STEP 1: Retrieve documents

    documents = retrieve_documents(
        query
    )

    if not documents:

        return (
            "No relevant information was found "
            "in the quotation database."
        )

    print(
        f"\nRetrieved {len(documents)} documents."
    )

    # STEP 2: Build context

    context = build_context(
        documents
    )

    print("\nRetrieved Context:")

    print(
        "\n" + context[:1000]
    )

    # STEP 3: Initialize Gemini

    llm = get_llm()

    # STEP 4: Create prompt

    prompt = f"""
You are an AI quotation assistant.

Your job is to answer customer questions using ONLY
the information provided in the context below.

Do not invent products, prices, suppliers, specifications,
warranties, or availability.

If the requested information is not available in the context,
clearly say that it is not available.

You should help recommend suitable products based on:

- Processor
- RAM
- Storage
- Price
- Warranty
- Availability
- Company quotation policy

CONTEXT:

{context}


CUSTOMER QUESTION:

{query}


Provide a clear and professional answer.
"""

    print("\nSending context to Gemini...")

    # STEP 5: Generate answer

    response = llm.invoke(
        prompt
    )

    return response.content


# ==========================================
# RUN RAG CHAIN
# ==========================================

if __name__ == "__main__":

    query = (
        "I need laptops with Intel Core i5, "
        "16GB RAM and 512GB SSD. "
        "Recommend suitable options."
    )

    answer = rag_chain(
        query
    )

    print("\n=================================")
    print("FINAL RAG ANSWER")
    print("=================================\n")

    print(answer)