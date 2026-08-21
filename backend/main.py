from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.graph import create_quotation_graph


app = FastAPI(
    title="Quotation Agent API",
    version="1.0.0"
)


class QuotationRequest(BaseModel):
    customer_name: str
    processor: str
    ram: str
    storage: str
    quantity: int
    max_budget: float


@app.get("/")
def home():
    return {
        "message": "Quotation Agent API is running successfully"
    }


@app.post("/generate-quotation")
def generate_quotation(request: QuotationRequest):

    try:

        # Create graph
        graph = create_quotation_graph()

        # Initial state
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

        # Run graph
        result = graph.invoke(initial_state)

        return {
            "customer_name": result.get("customer_name"),
            "selected_product": result.get("selected_product"),
            "pricing_details": result.get("pricing_details"),
            "quotation": result.get("quotation"),
            "approval_status": result.get("approval_status"),
            "pdf_path": result.get("pdf_path")
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )