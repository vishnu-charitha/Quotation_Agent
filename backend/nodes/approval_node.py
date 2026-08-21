def approval_node(state):

    print("\n--- APPROVAL NODE ---")

    quotation = state["quotation"]

    pricing_details = state["pricing_details"]

    final_total = pricing_details["final_total"]

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
        f"Final Total: ₹{final_total}"
    )

    # Example approval rule
    if final_total <= 1000000:
        approval_status = "approved"
    else:
        approval_status = "pending_manual_approval"

    return {
        "approval_status": approval_status
    }