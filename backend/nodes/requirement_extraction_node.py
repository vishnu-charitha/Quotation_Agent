import os
import json

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing in the .env file"
    )


# =========================================================
# INITIALIZE GEMINI
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)


# =========================================================
# REQUIREMENT EXTRACTION NODE
# =========================================================

def requirement_extraction_node(state):

    print("\n=================================")
    print("REQUIREMENT EXTRACTION NODE")
    print("=================================")

    query = state.get("query", "")

    if not query:
        raise ValueError("Customer query is missing")

    print(f"\nCustomer Query:\n{query}")


    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are an AI requirement extraction system.

Extract laptop quotation requirements from the
customer's natural language request.

Customer Request:

{query}


Return ONLY valid JSON.

Use exactly this format:

{{
    "customer_name": null,
    "processor": null,
    "ram": null,
    "storage": null,
    "quantity": null,
    "max_budget": null
}}

Rules:

1. Extract the processor exactly as mentioned.

2. Extract RAM in a format like:
   "8GB"
   "16GB"
   "32GB"

3. Extract storage in a format like:
   "256GB SSD"
   "512GB SSD"
   "1TB SSD"

4. Extract quantity as an integer.

5. Extract max_budget as a number without:
   - ₹
   - commas
   - currency symbols

6. If customer name is not mentioned, return null.

7. If any information is not mentioned,
   return null for that field.

8. Do not add explanations.

Return only JSON.
"""


    # =====================================================
    # CALL GEMINI
    # =====================================================

    try:

        response = llm.invoke(prompt)

        content = response.content.strip()

        print("\nGemini Raw Response:")
        print(content)


        # =================================================
        # REMOVE MARKDOWN CODE BLOCKS IF PRESENT
        # =================================================

        if content.startswith("```"):

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        # =================================================
        # CONVERT JSON STRING TO PYTHON DICTIONARY
        # =================================================

        requirements = json.loads(content)


        print("\nExtracted Requirements:")

        for key, value in requirements.items():
            print(f"{key}: {value}")


        return {
            "requirements": requirements
        }


    except Exception as error:

        print("\nREQUIREMENT EXTRACTION ERROR:")
        print(str(error))

        raise ValueError(
            f"Unable to extract customer requirements: {str(error)}"
        )