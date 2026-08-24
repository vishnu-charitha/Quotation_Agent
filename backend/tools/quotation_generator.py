from datetime import datetime, timedelta
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


# ==========================================
# GENERATE QUOTATION DATA
# ==========================================

def generate_quotation(
    customer_name,
    selected_product,
    pricing_details,
    approval_status,
    validity_days=7
):

    quotation_number = (
        "QT-"
        + datetime.now().strftime("%Y%m%d%H%M%S")
    )

    quotation_date = datetime.now()

    valid_until = (
        quotation_date
        + timedelta(days=validity_days)
    )

    quotation = {

        "quotation_number":
            quotation_number,

        "quotation_date":
            quotation_date.strftime("%Y-%m-%d"),

        "valid_until":
            valid_until.strftime("%Y-%m-%d"),

        "customer_name":
            customer_name,

        "product": {

            "product_id":
                selected_product["product_id"],

            "supplier":
                selected_product["supplier"],

            "brand":
                selected_product["brand"],

            "model":
                selected_product["model"],

            "processor":
                selected_product["processor"],

            "ram":
                selected_product["ram"],

            "storage":
                selected_product["storage"],

            "warranty":
                selected_product["warranty"]
        },

        "pricing":
            pricing_details,

        "status":
            "Generated",

        "approval_status":
            approval_status
    }

    return quotation


# ==========================================
# GENERATE QUOTATION PDF
# ==========================================

def generate_quotation_pdf(quotation):

    # Project root directory

    BASE_DIR = Path(__file__).resolve().parents[2]

    # Create generated_quotations folder

    output_dir = (
        BASE_DIR / "generated_quotations"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    # PDF file path

    quotation_number = (
        quotation["quotation_number"]
    )

    file_path = (
        output_dir
        / f"{quotation_number}.pdf"
    )

    # Create PDF

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=A4
    )

    width, height = A4

    y = height - 25 * mm


    # ==========================================
    # TITLE
    # ==========================================

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        y,
        "QUOTATION"
    )

    y -= 20 * mm


    # ==========================================
    # QUOTATION INFORMATION
    # ==========================================

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(
        20 * mm,
        y,
        f"Quotation Number: {quotation['quotation_number']}"
    )

    y -= 8 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Quotation Date: {quotation['quotation_date']}"
    )

    y -= 8 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Valid Until: {quotation['valid_until']}"
    )

    y -= 8 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Customer: {quotation['customer_name']}"
    )

    y -= 15 * mm


    # ==========================================
    # PRODUCT DETAILS
    # ==========================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        20 * mm,
        y,
        "PRODUCT DETAILS"
    )

    y -= 10 * mm

    product = quotation["product"]

    pdf.setFont(
        "Helvetica",
        11
    )

    product_details = [

        f"Product ID: {product['product_id']}",

        f"Supplier: {product['supplier']}",

        f"Brand: {product['brand']}",

        f"Model: {product['model']}",

        f"Processor: {product['processor']}",

        f"RAM: {product['ram']}",

        f"Storage: {product['storage']}",

        f"Warranty: {product['warranty']}"
    ]

    for detail in product_details:

        pdf.drawString(
            20 * mm,
            y,
            detail
        )

        y -= 8 * mm


    # ==========================================
    # PRICING DETAILS
    # ==========================================

    y -= 5 * mm

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        20 * mm,
        y,
        "PRICING DETAILS"
    )

    y -= 10 * mm

    pricing = quotation["pricing"]

    pdf.setFont(
        "Helvetica",
        11
    )

    pricing_details = [

        (
            "Supplier Price Per Unit: "
            f"Rs. {pricing['supplier_price_per_unit']:,.2f}"
        ),

        (
            f"Quantity: "
            f"{pricing['quantity']}"
        ),

        (
            "Profit Margin: "
            f"{pricing['profit_margin_percent']}%"
        ),

        (
            "Selling Price Per Unit: "
            f"Rs. {pricing['selling_price_per_unit']:,.2f}"
        ),

        (
            f"Subtotal: "
            f"Rs. {pricing['subtotal']:,.2f}"
        ),

        (
            f"GST ({pricing['gst_rate']}%): "
            f"Rs. {pricing['gst_amount']:,.2f}"
        )
    ]

    for detail in pricing_details:

        pdf.drawString(
            20 * mm,
            y,
            detail
        )

        y -= 8 * mm


    # ==========================================
    # FINAL TOTAL
    # ==========================================

    y -= 5 * mm

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        20 * mm,
        y,
        (
            "FINAL TOTAL: "
            f"Rs. {pricing['final_total']:,.2f}"
        )
    )

    y -= 15 * mm


    # ==========================================
    # APPROVAL STATUS
    # ==========================================

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        20 * mm,
        y,
        (
            "APPROVAL STATUS: "
            f"{quotation['approval_status']}"
        )
    )


    # ==========================================
    # FOOTER
    # ==========================================

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawCentredString(
        width / 2,
        15 * mm,
        "Thank you for your business."
    )


    # ==========================================
    # SAVE PDF
    # ==========================================

    pdf.save()

    return str(file_path)