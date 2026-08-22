import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing in .env")


print("Gemini API key loaded successfully.")


# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0
)


print("Testing Gemini API...\n")


response = llm.invoke(
    "Say hello. You are going to help build an AI quotation agent."
)


print("Gemini Response:")
print(response.content)