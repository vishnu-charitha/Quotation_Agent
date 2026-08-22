import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

ENV_PATH = BASE_DIR / ".env"


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(ENV_PATH)


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = "quotation_documents"


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# LOAD TXT FILE
# =========================================================

def load_txt_file(file_path: Path):

    print(f"\nChecking TXT: {file_path}")

    if not file_path.exists():
        print("TXT FILE NOT FOUND - SKIPPING")
        return []

    if file_path.stat().st_size == 0:
        print("TXT FILE IS EMPTY - SKIPPING")
        return []

    try:
        content = file_path.read_text(
            encoding="utf-8"
        )

        print(
            f"Characters found: {len(content)}"
        )

        if not content.strip():
            print("TXT FILE HAS NO CONTENT - SKIPPING")
            return []

        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name,
                "type": "text"
            }
        )

        print(
            f"Successfully loaded: {file_path.name}"
        )

        return [document]

    except Exception as error:

        print(
            f"ERROR LOADING {file_path.name}: {error}"
        )

        return []


# =========================================================
# LOAD PDF FILE
# =========================================================

def load_pdf_file(file_path: Path):

    print(f"\nChecking PDF: {file_path}")

    if not file_path.exists():
        print("PDF FILE NOT FOUND - SKIPPING")
        return []

    if file_path.stat().st_size == 0:
        print("PDF FILE IS EMPTY - SKIPPING")
        return []

    try:

        from langchain_community.document_loaders import (
            PyPDFLoader
        )

        loader = PyPDFLoader(
            str(file_path)
        )

        documents = loader.load()

        print(
            f"Successfully loaded "
            f"{len(documents)} pages from "
            f"{file_path.name}"
        )

        return documents

    except Exception as error:

        print(
            f"ERROR LOADING PDF "
            f"{file_path.name}: {error}"
        )

        return []


# =========================================================
# LOAD CSV FILE
# =========================================================

def load_csv_file(file_path: Path):

    print(f"\nChecking CSV: {file_path}")

    if not file_path.exists():
        print("CSV FILE NOT FOUND - SKIPPING")
        return []

    if file_path.stat().st_size == 0:
        print("CSV FILE IS EMPTY - SKIPPING")
        return []

    try:

        dataframe = pd.read_csv(
            file_path
        )

        if dataframe.empty:
            print("CSV HAS 0 ROWS - SKIPPING")
            return []

        documents = []

        for index, row in dataframe.iterrows():

            row_text = "\n".join(
                [
                    f"{column}: {value}"
                    for column, value
                    in row.items()
                ]
            )

            document = Document(
                page_content=row_text,
                metadata={
                    "source": file_path.name,
                    "row": int(index),
                    "type": "csv"
                }
            )

            documents.append(document)

        print(
            f"Successfully loaded "
            f"{len(documents)} rows from "
            f"{file_path.name}"
        )

        return documents

    except Exception as error:

        print(
            f"ERROR LOADING CSV "
            f"{file_path.name}: {error}"
        )

        return []


# =========================================================
# LOAD ALL DOCUMENTS
# =========================================================

def load_documents():

    print("\n=================================")
    print("LOADING DOCUMENTS")
    print("=================================")

    documents = []


    # TXT FILES

    txt_files = [
        "supplier_catalog.txt",
        "pricing_policy.txt",
        "company_policy.txt"
    ]

    for file_name in txt_files:

        file_path = DATA_DIR / file_name

        docs = load_txt_file(
            file_path
        )

        documents.extend(docs)


    # PDF FILES

    pdf_files = [
        "supplier_catalog.pdf"
    ]

    for file_name in pdf_files:

        file_path = DATA_DIR / file_name

        docs = load_pdf_file(
            file_path
        )

        documents.extend(docs)


    # CSV FILES

    csv_files = [
        "products.csv"
    ]

    for file_name in csv_files:

        file_path = DATA_DIR / file_name

        docs = load_csv_file(
            file_path
        )

        documents.extend(docs)


    print("\n=================================")

    print(
        f"TOTAL VALID DOCUMENTS: "
        f"{len(documents)}"
    )

    print("=================================")

    return documents


# =========================================================
# SPLIT DOCUMENTS INTO CHUNKS
# =========================================================

def split_documents(documents):

    print("\n=================================")
    print("SPLITTING DOCUMENTS")
    print("=================================")

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=100,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )


    chunks = splitter.split_documents(
        documents
    )


    print(
        f"\nTOTAL CHUNKS CREATED: "
        f"{len(chunks)}"
    )


    if chunks:

        print("\nSAMPLE CHUNK:\n")

        print(
            chunks[0].page_content
        )

        print("\nMETADATA:")

        print(
            chunks[0].metadata
        )


    return chunks


# =========================================================
# CONNECT TO QDRANT
# =========================================================

def get_qdrant_client():

    print("\n=================================")
    print("CONNECTING TO QDRANT")
    print("=================================")


    # CHECK URL

    if not QDRANT_URL:

        raise ValueError(
            "\nQDRANT_URL is missing.\n"
            "Please add it to your .env file."
        )


    # CHECK API KEY

    if not QDRANT_API_KEY:

        raise ValueError(
            "\nQDRANT_API_KEY is missing.\n"
            "Please add it to your .env file."
        )


    try:

        print(
            "\nCreating Qdrant client..."
        )


        client = QdrantClient(

            url=QDRANT_URL,

            api_key=QDRANT_API_KEY,

            timeout=60

        )


        print(
            "Testing Qdrant connection..."
        )


        collections = client.get_collections()


        print(
            "Connected to Qdrant successfully!"
        )


        print(
            f"Existing collections: "
            f"{len(collections.collections)}"
        )


        return client


    except Exception as error:

        print(
            "\n================================="
        )

        print(
            "FAILED TO CONNECT TO QDRANT"
        )

        print(
            "================================="
        )

        print(
            f"\nError: {error}"
        )

        print(
            "\nPossible reasons:"
        )

        print(
            "1. QDRANT_URL is incorrect"
        )

        print(
            "2. QDRANT_API_KEY is incorrect"
        )

        print(
            "3. Internet connection problem"
        )

        print(
            "4. SSL handshake timeout"
        )

        print(
            "5. Firewall or VPN is blocking the connection"
        )

        raise


# =========================================================
# STORE DOCUMENTS IN QDRANT
# =========================================================

def store_documents(chunks):

    print("\n=================================")
    print("STORING VECTORS IN QDRANT")
    print("=================================")


    if not chunks:

        raise ValueError(
            "No chunks available to store."
        )


    # CONNECT TO QDRANT

    client = get_qdrant_client()


    # GENERATE TEST EMBEDDING

    print(
        "\nGenerating test embedding..."
    )


    test_embedding = embeddings.embed_query(
        "test"
    )


    vector_size = len(
        test_embedding
    )


    print(
        f"Embedding vector size: "
        f"{vector_size}"
    )


    # CHECK EXISTING COLLECTIONS

    print(
        "\nChecking existing collections..."
    )


    existing_collections = client.get_collections()


    collection_names = [

        collection.name

        for collection

        in existing_collections.collections

    ]


    # DELETE OLD COLLECTION

    if COLLECTION_NAME in collection_names:

        print(
            f"\nDeleting existing collection: "
            f"{COLLECTION_NAME}"
        )


        client.delete_collection(

            collection_name=COLLECTION_NAME

        )


        print(
            "Old collection deleted."
        )


    # CREATE NEW COLLECTION

    print(
        "\nCreating Qdrant collection..."
    )


    client.create_collection(

        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(

            size=vector_size,

            distance=Distance.COSINE

        )

    )


    print(
        "Collection created successfully!"
    )


    # PREPARE TEXTS

    texts = [

        chunk.page_content

        for chunk in chunks

    ]


    # GENERATE EMBEDDINGS

    print(
        "\nGenerating embeddings for documents..."
    )


    vectors = embeddings.embed_documents(
        texts
    )


    print(
        f"Generated {len(vectors)} embeddings."
    )


    # PREPARE QDRANT POINTS

    print(
        "\nPreparing vectors for upload..."
    )


    points = []


    for index, chunk in enumerate(chunks):

        point = PointStruct(

            id=index,

            vector=vectors[index],

            payload={

                "page_content":
                    chunk.page_content,

                "metadata":
                    chunk.metadata

            }

        )


        points.append(
            point
        )


    # UPLOAD VECTORS

    print(
        "\nUploading vectors to Qdrant..."
    )


    client.upsert(

        collection_name=COLLECTION_NAME,

        points=points

    )


    print("\n=================================")

    print(
        "SUCCESS! VECTORS STORED IN QDRANT"
    )

    print("=================================")


    print(
        f"\nCollection Name: "
        f"{COLLECTION_NAME}"
    )


    print(
        f"Total Vectors Stored: "
        f"{len(points)}"
    )


# =========================================================
# MAIN INGESTION FUNCTION
# =========================================================

def ingest_documents():

    print("\n=================================")
    print("QUOTATION AGENT RAG INGESTION")
    print("=================================")


    # STEP 1: LOAD DOCUMENTS

    documents = load_documents()


    if not documents:

        raise ValueError(
            "\nNo documents were loaded.\n"
            "Please add valid files "
            "inside the data folder."
        )


    # STEP 2: SPLIT DOCUMENTS

    chunks = split_documents(
        documents
    )


    if not chunks:

        raise ValueError(
            "\nNo chunks were created.\n"
            "Check your document content."
        )


    # STEP 3: STORE VECTORS

    store_documents(
        chunks
    )


# =========================================================
# RUN INGESTION
# =========================================================

if __name__ == "__main__":

    ingest_documents()