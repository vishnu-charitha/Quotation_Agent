from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.agent import quotation_agent


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Quotation Agent API",
    version="1.0.0",
    description="AI-powered quotation generation using LangGraph and RAG"
)


# =========================================================
# REQUEST MODELS
# =========================================================

class QuotationRequest(
    BaseModel
):

    customer_name: str
    processor: str
    ram: str
    storage: str
    quantity: int
    max_budget: float


class AgentRequest(
    BaseModel
):

    query: str


# =========================================================
# HOME ROUTE
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Quotation Agent API is running"
    }


# =========================================================
# GENERATE QUOTATION
# =========================================================

@app.post("/generate-quotation")
def generate_quotation(
    request: QuotationRequest
):

    try:

        # -------------------------------------------------
        # SAMPLE PRODUCT DATA
        # -------------------------------------------------

        product = {
            "supplier": "Dell Technologies",
            "product": "Dell Inspiron 15",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "price": 55000,
            "price_per_unit": 55000,
            "warranty": "2 Years",
            "availability": "In Stock"
        }


        # -------------------------------------------------
        # CALCULATE PRICE
        # -------------------------------------------------

        price_per_unit = product["price"]

        total_price = (
            price_per_unit
            * request.quantity
        )


        # -------------------------------------------------
        # CHECK BUDGET
        # -------------------------------------------------

        if total_price <= request.max_budget:

            approval_status = "APPROVED"

        else:

            approval_status = "REJECTED"


        # -------------------------------------------------
        # CREATE QUOTATION
        # -------------------------------------------------

        quotation = f"""
========================================
             QUOTATION
========================================

Customer Name: {request.customer_name}

----------------------------------------
PRODUCT DETAILS
----------------------------------------

Supplier: {product["supplier"]}

Product: {product["product"]}

Processor: {product["processor"]}

RAM: {product["ram"]}

Storage: {product["storage"]}

Warranty: {product["warranty"]}

Availability: {product["availability"]}


----------------------------------------
PRICING DETAILS
----------------------------------------

Price Per Unit: ₹{price_per_unit}

Quantity: {request.quantity}

Total Price: ₹{total_price}

Maximum Budget: ₹{request.max_budget}


----------------------------------------
STATUS
----------------------------------------

Approval Status: {approval_status}

========================================

Thank you for choosing our services.
"""


        return {

            "customer_name":
                request.customer_name,

            "selected_product":
                product,

            "pricing_details": {

                "price_per_unit":
                    price_per_unit,

                "quantity":
                    request.quantity,

                "total_price":
                    total_price,

                "max_budget":
                    request.max_budget
            },

            "quotation":
                quotation,

            "approval_status":
                approval_status
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# AGENT QUOTATION
# =========================================================

@app.post("/agent-quotation")
def agent_quotation(
    request: AgentRequest
):

    try:

        print("\n=================================")
        print("AGENT RECEIVED QUERY")
        print("=================================\n")

        print(request.query)


        # -----------------------------------------------
        # RUN LANGGRAPH
        # -----------------------------------------------

        result = quotation_graph.invoke(
            {
                "query":
                    request.query,

                "documents":
                    [],

                "context":
                    "",

                "answer":
                    ""
            }
        )


        # -----------------------------------------------
        # RETURN RESPONSE
        # -----------------------------------------------

        return {

            "query":
                request.query,

            "response":
                result.get(
                    "answer",
                    "No response generated."
                ),

            "retrieved_documents":
                len(
                    result.get(
                        "documents",
                        []
                    )
                )
        }


    except Exception as e:

        print(
            "\nAGENT ERROR:",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )