from datetime import datetime, timedelta
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def generate_quotation(
    customer_name,
    selected_product,
    pricing_details,
    validity_days=7
):
    """
    Generate quotation data.
    """

    quotation_number = (
        "QT-"
        + datetime.now().strftime("%Y%m%d%H%M%S")
    )

    quotation_date = datetime.now()

    valid_until = (
        quotation_date + timedelta(days=validity_days)
    )

    quotation = {
        "quotation_number": quotation_number,

        "quotation_date": quotation_date.strftime("%Y-%m-%d"),

        "valid_until": valid_until.strftime("%Y-%m-%d"),

        "customer_name": customer_name,

        "product": {
            "product_id": selected_product["product_id"],
            "brand": selected_product["brand"],
            "model": selected_product["model"],
            "processor": selected_product["processor"],
            "ram": selected_product["ram"],
            "storage": selected_product["storage"],
            "warranty": selected_product["warranty"]
        },

        "pricing": pricing_details,

        "status": "Generated"
    }

    return quotation


def generate_quotation_pdf(quotation):
    """
    Generate a PDF file from quotation data.
    """

    output_folder = "generated_quotations"

    os.makedirs(output_folder, exist_ok=True)

    file_name = (
        f"{quotation['quotation_number']}.pdf"
    )

    file_path = os.path.join(
        output_folder,
        file_name
    )

    document = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph(
        "<b>QUOTATION</b>",
        styles["Title"]
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # Quotation information
    quotation_info = [
        [
            "Quotation Number",
            quotation["quotation_number"]
        ],
        [
            "Quotation Date",
            quotation["quotation_date"]
        ],
        [
            "Valid Until",
            quotation["valid_until"]
        ],
        [
            "Customer",
            quotation["customer_name"]
        ]
    ]

    info_table = Table(
        quotation_info,
        colWidths=[2 * inch, 4 * inch]
    )

    info_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    elements.append(info_table)
    elements.append(Spacer(1, 25))

    # Product title
    product_title = Paragraph(
        "<b>Product Details</b>",
        styles["Heading2"]
    )

    elements.append(product_title)
    elements.append(Spacer(1, 10))

    product = quotation["product"]

    product_data = [
        ["Product ID", product["product_id"]],
        ["Brand", product["brand"]],
        ["Model", product["model"]],
        ["Processor", product["processor"]],
        ["RAM", product["ram"]],
        ["Storage", product["storage"]],
        ["Warranty", product["warranty"]]
    ]

    product_table = Table(
        product_data,
        colWidths=[2 * inch, 4 * inch]
    )

    product_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    elements.append(product_table)
    elements.append(Spacer(1, 25))

    # Pricing title
    pricing_title = Paragraph(
        "<b>Pricing Details</b>",
        styles["Heading2"]
    )

    elements.append(pricing_title)
    elements.append(Spacer(1, 10))

    pricing = quotation["pricing"]

    pricing_data = [
        [
            "Supplier Price Per Unit",
            f"Rs. {pricing['supplier_price_per_unit']:,.2f}"
        ],
        [
            "Quantity",
            str(pricing["quantity"])
        ],
        [
            "Profit Margin",
            f"{pricing['profit_margin_percent']}%"
        ],
        [
            "Selling Price Per Unit",
            f"Rs. {pricing['selling_price_per_unit']:,.2f}"
        ],
        [
            "Subtotal",
            f"Rs. {pricing['subtotal']:,.2f}"
        ],
        [
            "GST",
            f"{pricing['gst_rate']}%"
        ],
        [
            "GST Amount",
            f"Rs. {pricing['gst_amount']:,.2f}"
        ],
        [
            "Final Total",
            f"Rs. {pricing['final_total']:,.2f}"
        ]
    ]

    pricing_table = Table(
        pricing_data,
        colWidths=[3 * inch, 3 * inch]
    )

    pricing_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "BACKGROUND",
                (0, -1),
                (-1, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, -1),
                (-1, -1),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )

    elements.append(pricing_table)
    elements.append(Spacer(1, 30))

    # Status
    status = Paragraph(
        f"<b>Status:</b> {quotation['status']}",
        styles["Normal"]
    )

    elements.append(status)

    # Build PDF
    document.build(elements)

    return file_path