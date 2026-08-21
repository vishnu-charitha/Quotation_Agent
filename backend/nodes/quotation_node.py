from backend.tools.quotation_generator import generate_quotation


def quotation_node(state):

    print("\n--- QUOTATION NODE ---")

    quotation = generate_quotation(
        customer_name=state["customer_name"],
        selected_product=state["selected_product"],
        pricing_details=state["pricing_details"],
        validity_days=7
    )

    print("\nQuotation Generated:")

    print(
        f"Quotation Number: "
        f"{quotation['quotation_number']}"
    )

    print(
        f"Customer: "
        f"{quotation['customer_name']}"
    )

    print(
        f"Status: "
        f"{quotation['status']}"
    )

    return {
        "quotation": quotation
    }