import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(
    BASE_DIR / ".env"
)


# ==========================================
# GET GEMINI API KEY
# ==========================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY is missing in the .env file"
    )


# ==========================================
# CREATE EMBEDDING MODEL
# ==========================================

def get_embeddings():

    print(
        "\nInitializing Gemini Embedding Model..."
    )

    embeddings = GoogleGenerativeAIEmbeddings(

        model="models/gemini-embedding-001",

        google_api_key=GEMINI_API_KEY

    )

    return embeddings