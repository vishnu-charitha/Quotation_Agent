from typing import TypedDict, Dict, Any, Optional


class QuotationState(TypedDict, total=False):

    customer_name: str

    requirements: Dict[str, Any]

    selected_product: Dict[str, Any]

    pricing_details: Dict[str, Any]

    quotation: Dict[str, Any]

    approval_status: str

    pdf_path: Optional[str]