from typing import TypedDict, Dict, Any, List


class QuotationState(TypedDict, total=False):

    # Original customer query
    query: str

    # Customer name
    customer_name: str

    # Extracted requirements
    requirements: Dict[str, Any]

    # Documents retrieved from RAG
    retrieved_documents: List[Dict[str, Any]]

    # Selected product
    selected_product: Dict[str, Any]

    # Pricing information
    pricing_details: Dict[str, Any]

    # Approval result
    approval_status: str

    # Rejection reason
    rejection_reason: str

    # Generated quotation
    quotation: Dict[str, Any]

    # Generated PDF path
    pdf_path: str