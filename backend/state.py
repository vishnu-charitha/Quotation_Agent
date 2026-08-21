from typing import TypedDict, Optional, List, Dict, Any


class QuotationState(TypedDict, total=False):

    customer_name: str

    requirements: Dict[str, Any]

    matching_products: List[Dict[str, Any]]

    ranked_products: List[Dict[str, Any]]

    selected_product: Optional[Dict[str, Any]]

    pricing_details: Optional[Dict[str, Any]]

    quotation: Optional[Dict[str, Any]]

    approval_status: Optional[str]