import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.rag.retriever import get_rag_context


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")


# =========================================================
# GET GEMINI API KEY
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing in .env file"
    )


# =========================================================
# INITIALIZE GEMINI MODEL
# =========================================================

print("Initializing Gemini model...")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)


# =========================================================
# QUOTATION AGENT
# =========================================================

class QuotationAgent:

    def invoke(self, state):

        messages = state.get(
            "messages",
            []
        )

        if not messages:
            raise ValueError(
                "No message provided to the agent"
            )

        # Get latest user query
        user_message = messages[-1]

        # Support dictionary messages
        if isinstance(user_message, dict):

            query = user_message.get(
                "content",
                ""
            )

        else:

            query = str(
                user_message.content
            )


        print("\n=================================")
        print("AGENT RECEIVED QUERY")
        print("=================================\n")

        print(query)


        # =================================================
        # RETRIEVE RAG CONTEXT
        # =================================================

        print("\nRetrieving relevant documents...")

        context = get_rag_context(
            query=query,
            limit=5
        )


        # =================================================
        # CREATE PROMPT
        # =================================================

        prompt = f"""
You are an AI-powered quotation assistant.

Your job is to help customers find suitable laptop products
and provide quotation-related information.

Use ONLY the information provided in the retrieved context.

If the requested product information is not available,
clearly say that no suitable product was found.

Do not invent suppliers, products, prices, specifications,
warranties, or availability.

Customer Query:

{query}


Retrieved Product Information:

{context}


Instructions:

1. Understand the customer's requirements.
2. Find suitable products from the retrieved information.
3. Compare products when multiple options exist.
4. Consider processor, RAM, storage, quantity, and budget.
5. Calculate total cost when quantity is provided.
6. Clearly mention whether the budget is sufficient.
7. Recommend the most suitable option.
8. Keep the answer professional and easy to understand.

Generate the final quotation recommendation.
"""


        # =================================================
        # CALL GEMINI
        # =================================================

        print("\nSending request to Gemini...")

        response = llm.invoke(
            prompt
        )


        # =================================================
        # RETURN AGENT RESPONSE
        # =================================================

        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": response.content
                }
            ]
        }


# =========================================================
# CREATE AGENT INSTANCE
# =========================================================

agent = QuotationAgent()