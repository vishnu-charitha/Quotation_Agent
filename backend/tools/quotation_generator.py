from datetime import datetime, timedelta


def generate_quotation(
    customer_name,
    selected_product,
    pricing_details,
    validity_days=7
):
    """
    Generate a structured quotation.
    """

    quotation_date = datetime.now()
    valid_until = quotation_date + timedelta(days=validity_days)

    quotation_number = (
        f"QT-{quotation_date.strftime('%Y%m%d%H%M%S')}"
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

        "pricing": {
            "supplier_price_per_unit":
                pricing_details["supplier_price_per_unit"],

            "quantity":
                pricing_details["quantity"],

            "profit_margin_percent":
                pricing_details["profit_margin_percent"],

            "selling_price_per_unit":
                pricing_details["selling_price_per_unit"],

            "subtotal":
                pricing_details["subtotal"],

            "gst_rate":
                pricing_details["gst_rate"],

            "gst_amount":
                pricing_details["gst_amount"],

            "final_total":
                pricing_details["final_total"]
        },

        "status": "Generated"
    }

    return quotation