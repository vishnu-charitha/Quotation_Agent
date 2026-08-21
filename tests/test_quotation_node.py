from backend.nodes.quotation_node import quotation_node


def test_quotation_node():

    state = {
        "customer_name": "ABC Technologies",

        "selected_product": {
            "product_id": "L002",
            "brand": "Lenovo",
            "model": "ThinkPad E14",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "warranty": "3 Years"
        },

        "pricing_details": {
            "supplier_price_per_unit": 57000.0,
            "quantity": 15,
            "profit_margin_percent": 10,
            "selling_price_per_unit": 62700.0,
            "subtotal": 940500.0,
            "gst_rate": 18,
            "gst_amount": 169290.0,
            "final_total": 1109790.0
        }
    }

    result = quotation_node(state)

    quotation = result["quotation"]

    print("\nGenerated Quotation:")

    print(f"Quotation Number: {quotation['quotation_number']}")
    print(f"Customer: {quotation['customer_name']}")
    print(f"Status: {quotation['status']}")

    assert quotation["status"] == "Generated"