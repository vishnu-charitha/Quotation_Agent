def approval_node(state):

    print("\n--- APPROVAL NODE ---")

    quotation = state["quotation"]
    pricing_details = state["pricing_details"]

    print("\nQuotation ready for approval:")

    print(
        f"Quotation Number: "
        f"{quotation['quotation_number']}"
    )

    print(
        f"Customer: "
        f"{quotation['customer_name']}"
    )

    print(
        f"Final Total: "
        f"₹{pricing_details['final_total']}"
    )

    return {}