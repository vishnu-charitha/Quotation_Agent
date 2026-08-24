from backend.tools.quotation_generator import generate_quotation


def quotation_node(state):

    print("\n==============================")
    print("QUOTATION NODE")
    print("==============================")

    quotation = generate_quotation(
        customer_name=state["customer_name"],
        selected_product=state["selected_product"],
        pricing_details=state["pricing_details"],
        approval_status=state["approval_status"],
        validity_days=7
    )

    print("\nQuotation Generated Successfully")

    print(
        f"Quotation Number: "
        f"{quotation['quotation_number']}"
    )

    print(
        f"Customer: "
        f"{quotation['customer_name']}"
    )

    print(
        f"Approval Status: "
        f"{quotation['approval_status']}"
    )

    return {
        "quotation": quotation
    }