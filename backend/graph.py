import os
from pathlib import Path
from typing import TypedDict, List, Dict, Any

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

from backend.rag.retriever import retrieve_documents


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / ".env")


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

print("Initializing Gemini model...")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)


# =========================================================
# DEFINE GRAPH STATE
# =========================================================

class AgentState(TypedDict):

    query: str

    documents: List[Dict[str, Any]]

    context: str

    answer: str


# =========================================================
# NODE 1: RETRIEVE DOCUMENTS
# =========================================================

def retrieve_node(
    state: AgentState
):

    print("\nRetrieving relevant documents...")

    query = state["query"]

    documents = retrieve_documents(
        query=query,
        limit=3
    )

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        content = document.get(
            "content",
            ""
        )

        score = document.get(
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

    context = "\n\n".join(
        context_parts
    )

    if not context.strip():

        context = (
            "No relevant product information "
            "was found in the knowledge base."
        )

    return {
        "documents": documents,
        "context": context
    }


# =========================================================
# NODE 2: GENERATE RESPONSE
# =========================================================

def generate_node(
    state: AgentState
):

    print("\nSending request to Gemini...")

    query = state["query"]

    context = state["context"]

    prompt = f"""
You are an AI-powered quotation assistant.

Your task is to generate a professional quotation
based ONLY on the retrieved product information.

Do not invent product names, suppliers, prices,
specifications, warranty information, or availability.

--------------------------------------------------

CUSTOMER REQUIREMENT:

{query}

--------------------------------------------------

RETRIEVED PRODUCT INFORMATION:

{context}

--------------------------------------------------

INSTRUCTIONS:

1. Understand the customer's requirements.

2. Analyze the retrieved products.

3. Select the best matching product.

4. Extract the product specifications.

5. Identify the quantity requested.

6. Identify the maximum budget.

7. Calculate:

   Total Price =
   Price Per Unit × Quantity

8. Compare the total price with the customer's budget.

9. If the total price is within the budget:

   Approval Status: APPROVED

10. If the total price exceeds the budget:

   Approval Status: REJECTED

11. Clearly format the response with:

CUSTOMER DETAILS

PRODUCT DETAILS

PRICING DETAILS

BUDGET ANALYSIS

APPROVAL STATUS

12. If there is not enough information in the retrieved
documents, clearly say that.

Return only the final quotation.
"""

    response = llm.invoke(
        prompt
    )

    # =====================================================
    # SAFELY EXTRACT RESPONSE CONTENT
    # =====================================================

    if hasattr(
        response,
        "content"
    ):

        answer = response.content

    elif isinstance(
        response,
        dict
    ):

        answer = response.get(
            "content",
            str(response)
        )

    else:

        answer = str(response)

    return {
        "answer": answer
    }


# =========================================================
# CREATE LANGGRAPH WORKFLOW
# =========================================================

workflow = StateGraph(
    AgentState
)


# =========================================================
# ADD NODES
# =========================================================

workflow.add_node(
    "retrieve",
    retrieve_node
)

workflow.add_node(
    "generate",
    generate_node
)


# =========================================================
# SET ENTRY POINT
# =========================================================

workflow.set_entry_point(
    "retrieve"
)


# =========================================================
# ADD EDGES
# =========================================================

workflow.add_edge(
    "retrieve",
    "generate"
)

workflow.add_edge(
    "generate",
    END
)


# =========================================================
# COMPILE GRAPH
# =========================================================

quotation_graph = workflow.compile()