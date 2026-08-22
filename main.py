from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from backend.schemas import QuotationRequest
from backend.graph import quotation_graph
from backend.agent import agent

from backend.rag.rag_chain import rag_chain

from pydantic import BaseModel


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Quotation Agent API",
    version="1.0.0",
    description="AI-powered quotation generation using LangGraph, RAG, Qdrant and Gemini"
)


# =========================================================
# HOME ENDPOINT
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Quotation Agent API is running successfully"
    }


# =========================================================
# STRUCTURED QUOTATION REQUEST
# =========================================================

@app.post("/generate-quotation")
def generate_quotation(request: QuotationRequest):

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

    # Run LangGraph workflow
    result = quotation_graph.invoke(initial_state)

    return {

        "customer_name": result.get("customer_name"),

        "selected_product": result.get("selected_product"),

        "pricing_details": result.get("pricing_details"),

        "quotation": result.get("quotation"),

        "approval_status": result.get("approval_status"),

        "pdf_path": result.get("pdf_path")
    }


# =========================================================
# DOWNLOAD QUOTATION PDF
# =========================================================

@app.get("/download-quotation/{quotation_number}")
def download_quotation(quotation_number: str):

    file_path = Path(
        "generated_quotations"
    ) / f"{quotation_number}.pdf"

    print(f"Looking for PDF at: {file_path}")

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Quotation PDF not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{quotation_number}.pdf"
    )


# =========================================================
# AGENT REQUEST SCHEMA
# =========================================================

class AgentRequest(BaseModel):

    query: str


# =========================================================
# LLM AGENT QUOTATION ENDPOINT
# =========================================================


@app.post("/agent-quotation")
def agent_quotation(request: AgentRequest):

    try:

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.query
                    }
                ]
            }
        )

        final_message = result["messages"][-1]

        return {
            "query": request.query,
            "response": final_message["content"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )