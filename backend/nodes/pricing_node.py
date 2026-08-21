from backend.services.pricing_service import calculate_price


def pricing_node(state):

    print("\n--- PRICING NODE ---")

    selected_product = state["selected_product"]
    requirements = state["requirements"]

    quantity = requirements["quantity"]

    pricing = calculate_price(
        supplier_price=selected_product["supplier_price"],
        quantity=quantity,
        profit_margin=10,
        gst_rate=18
    )

    print("\nPricing Details:")

    for key, value in pricing.items():
        print(f"{key}: {value}")

    return {
        "pricing_details": pricing
    }