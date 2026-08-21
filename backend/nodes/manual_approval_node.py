def manual_approval_node(state):

    print("\n--- MANUAL APPROVAL NODE ---")

    quotation = state["quotation"]

    print(
        f"Quotation {quotation['quotation_number']} "
        "requires manual approval."
    )

    return {
        "approval_status": "pending_manual_approval"
    }