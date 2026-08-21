from pydantic import BaseModel
from typing import Optional


class QuotationRequest(BaseModel):
    customer_name: str
    processor: str
    ram: str
    storage: str
    quantity: int
    max_budget: float


class SelectedProduct(BaseModel):
    product_id: str
    supplier: str
    brand: str
    model: str
    processor: str
    ram: str
    storage: str
    price: float
    warranty: str


class PricingDetails(BaseModel):
    supplier_price_per_unit: float
    quantity: int
    profit_margin_percent: float
    profit_amount_per_unit: float
    selling_price_per_unit: float
    subtotal: float
    gst_rate: float
    gst_amount: float
    final_total: float


class QuotationProduct(BaseModel):
    product_id: str
    supplier: str
    brand: str
    model: str
    processor: str
    ram: str
    storage: str
    warranty: str


class Quotation(BaseModel):
    quotation_number: str
    quotation_date: str
    valid_until: str
    customer_name: str
    product: QuotationProduct
    pricing: PricingDetails
    status: str


class QuotationResponse(BaseModel):
    customer_name: str
    selected_product: SelectedProduct
    pricing_details: PricingDetails
    quotation: Quotation
    approval_status: str
    pdf_path: Optional[str] = None