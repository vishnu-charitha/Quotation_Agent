from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from backend.quotation_graph import quotation_graph


# ==============================
# FASTAPI APP
# ==============================

app = FastAPI(
    title="Quotation Agent API",
    description="AI-Powered Product Quotation Generator",
    version="1.0.0"
)


# ==============================
# CORS CONFIGURATION
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# REQUEST MODEL
# ==============================

class QuotationRequest(BaseModel):
    query: str


# ==============================
# HOME ENDPOINT
# ==============================

@app.get("/")
def home():
    return {
        "message": "Quotation Agent API is running successfully"
    }


# ==============================
# GENERATE QUOTATION
# ==============================

@app.post("/generate-quotation")
def generate_quotation(request: QuotationRequest):

    print("\n=================================")
    print("QUOTATION REQUEST RECEIVED")
    print("=================================\n")

    print("Customer Query:")
    print(request.query)

    try:

        # Initial state for LangGraph
        initial_state = {
            "query": request.query
        }

        # Run the quotation workflow
        result = quotation_graph.invoke(initial_state)

        # Check whether a product was found
        if not result.get("selected_product"):

            raise HTTPException(
                status_code=400,
                detail="No matching product found for the requested requirements."
            )

        # Check approval status
        approval_status = result.get("approval_status")

        if approval_status != "APPROVED":

            return {
                "status": "rejected",
                "message": "Quotation could not be approved within the customer's budget.",
                "customer_name": result.get("customer_name"),
                "requirements": result.get("requirements"),
                "selected_product": result.get("selected_product"),
                "pricing_details": result.get("pricing_details"),
                "approval_status": approval_status
            }

        # Successful quotation
        return {
            "status": "success",

            "customer_name": result.get("customer_name"),

            "requirements": result.get("requirements"),

            "selected_product": result.get("selected_product"),

            "pricing_details": result.get("pricing_details"),

            "quotation": result.get("quotation"),

            "approval_status": approval_status,

            "pdf_path": result.get("pdf_path")
        }

    except HTTPException:
        raise

    except Exception as e:

        print("\n=================================")
        print("QUOTATION ERROR")
        print("=================================\n")

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==============================
# DOWNLOAD QUOTATION PDF
# ==============================

@app.get("/download-quotation/{quotation_number}")
def download_quotation(quotation_number: str):

    pdf_folder = Path("generated_quotations")

    pdf_file = pdf_folder / f"{quotation_number}.pdf"

    if not pdf_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Quotation PDF not found"
        )

    return FileResponse(
        path=pdf_file,
        media_type="application/pdf",
        filename=f"{quotation_number}.pdf"
    )