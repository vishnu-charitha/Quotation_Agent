from backend.tools.price_calculator import calculate_price


def pricing_node(state):

    print("\n--- PRICING NODE ---")

    selected_product = state["selected_product"]

    requirements = state["requirements"]

    quantity = requirements["quantity"]

    pricing_details = calculate_price(
        selected_product["price"],
        quantity
    )

    print("\nPricing Details:")

    for key, value in pricing_details.items():
        print(f"{key}: {value}")

    return {
        "pricing_details": pricing_details
    }