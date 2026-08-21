def approval_router(state):

    pricing_details = state["pricing_details"]

    final_total = pricing_details["final_total"]

    print("\n--- APPROVAL DECISION ---")
    print(f"Final Total: ₹{final_total}")

    if final_total <= 1000000:
        print("Decision: AUTO APPROVE")

        return "approved"

    else:
        print("Decision: MANUAL REVIEW REQUIRED")

        return "manual_review"