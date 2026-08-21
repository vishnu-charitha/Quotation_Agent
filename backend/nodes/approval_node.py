def approval_node(state):

    print("\n--- APPROVAL NODE ---")

    quotation = state["quotation"]
    pricing_details = state["pricing_details"]

    print("\nQuotation ready for approval:")
    print(f"Quotation Number: {quotation['quotation_number']}")
    print(f"Customer: {quotation['customer_name']}")
    print(f"Final Total: ₹{pricing_details['final_total']}")

    approval_status = "approved"

    print(f"\nApproval Status: {approval_status.upper()}")

    return {
        "approval_status": approval_status
    }