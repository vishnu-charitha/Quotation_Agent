from datetime import datetime, timedelta


def generate_quotation(
    customer_name,
    selected_product,
    pricing_details,
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

        "quotation_number": quotation_number,

        "quotation_date":
            quotation_date.strftime("%Y-%m-%d"),

        "valid_until":
            valid_until.strftime("%Y-%m-%d"),

        "customer_name": customer_name,

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

        "pricing": pricing_details,

        "status": "Generated"
    }

    return quotation


def generate_quotation_pdf(
    quotation,
    pricing_details
):

    import os
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    os.makedirs(
        "generated_quotations",
        exist_ok=True
    )

    quotation_number = quotation["quotation_number"]

    file_path = (
        f"generated_quotations/{quotation_number}.pdf"
    )

    pdf = canvas.Canvas(
        file_path,
        pagesize=A4
    )

    width, height = A4

    y = height - 60

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        200,
        y,
        "QUOTATION"
    )

    y -= 50

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        f"Quotation Number: {quotation['quotation_number']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Customer: {quotation['customer_name']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Quotation Date: {quotation['quotation_date']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Valid Until: {quotation['valid_until']}"
    )

    y -= 50

    product = quotation["product"]

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Product Details"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        f"Product ID: {product['product_id']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Brand: {product['brand']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Model: {product['model']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Processor: {product['processor']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"RAM: {product['ram']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Storage: {product['storage']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Warranty: {product['warranty']}"
    )

    y -= 50

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Pricing Details"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        f"Quantity: {pricing_details['quantity']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Price Per Unit: Rs.{pricing_details['selling_price_per_unit']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Subtotal: Rs.{pricing_details['subtotal']}"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"GST: Rs.{pricing_details['gst_amount']}"
    )

    y -= 30

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        f"FINAL TOTAL: Rs.{pricing_details['final_total']}"
    )

    pdf.save()

    return file_path