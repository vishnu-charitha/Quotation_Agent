def manual_review_node(state):

    print("\n--- MANUAL REVIEW NODE ---")

    quotation = state["quotation"]
    pricing_details = state["pricing_details"]

    print("\nQuotation requires manual review:")
    print(f"Quotation Number: {quotation['quotation_number']}")
    print(f"Customer: {quotation['customer_name']}")
    print(f"Final Total: ₹{pricing_details['final_total']}")

    review_status = "needs_review"

    print(f"\nReview Status: {review_status.upper()}")

    return {
        "approval_status": review_status
    }