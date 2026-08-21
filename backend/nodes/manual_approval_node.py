def manual_approval_node(state):

    print("\n--- MANUAL APPROVAL NODE ---")

    quotation = state["quotation"]

    print(
        f"Quotation "
        f"{quotation['quotation_number']} "
        f"requires manual approval."
    )

    return {
        "approval_status": "pending_manual_approval"
    }