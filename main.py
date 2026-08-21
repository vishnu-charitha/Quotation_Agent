from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from backend.schemas import (
    QuotationRequest,
    QuotationResponse
)

from backend.graph import create_quotation_graph


app = FastAPI(
    title="Quotation Agent API",
    description="AI-powered quotation generation using LangGraph",
    version="1.0.0"
)


# --------------------------------
# HOME ENDPOINT
# --------------------------------

@app.get("/")
def home():
    return {
        "message": "Quotation Agent API is running successfully"
    }


# --------------------------------
# GENERATE QUOTATION
# --------------------------------

@app.post(
    "/generate-quotation",
    response_model=QuotationResponse,
    summary="Generate Quotation"
)
def generate_quotation(request: QuotationRequest):

    try:

        graph = create_quotation_graph()

        initial_state = {
            "customer_name": request.customer_name,

            "requirements": {
                "processor": request.processor,
                "ram": request.ram,
                "storage": request.storage,
                "quantity": request.quantity,
                "max_budget": request.max_budget
            }
        }

        result = graph.invoke(initial_state)

        return {
            "customer_name": result["customer_name"],
            "selected_product": result["selected_product"],
            "pricing_details": result["pricing_details"],
            "quotation": result["quotation"],
            "approval_status": result["approval_status"],
            "pdf_path": result.get("pdf_path")
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )




# ----------------------------
# DOWNLOAD QUOTATION PDF
# ----------------------------

# ----------------------------
# DOWNLOAD QUOTATION PDF
# ----------------------------

@app.get(
    "/download-quotation/{quotation_number}",
    response_class=FileResponse,
    summary="Download Quotation PDF"
)
def download_quotation(quotation_number: str):

    pdf_path = os.path.join(
        "generated_quotations",
        f"{quotation_number}.pdf"
    )

    print("Looking for PDF at:", pdf_path)

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail=f"Quotation PDF not found at: {pdf_path}"
        )

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{quotation_number}.pdf"
    )