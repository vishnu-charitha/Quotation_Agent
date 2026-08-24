def alternative_suggestion_node(state):

    print("\n==============================")
    print("ALTERNATIVE SUGGESTION NODE")
    print("==============================")

    requirements = state["requirements"]

    selected_product = state["selected_product"]

    pricing_details = state["pricing_details"]

    max_budget = requirements["max_budget"]

    final_total = pricing_details["final_total"]

    additional_budget_required = max(
        0,
        final_total - max_budget
    )

    product_name = (
        f"{selected_product['brand']} "
        f"{selected_product['model']}"
    )

    suggestion = {

        "message": (
            "The requested configuration exceeds "
            "the customer's maximum budget."
        ),

        "cheapest_available_product": product_name,

        "customer_budget": max_budget,

        "required_total": final_total,

        "additional_budget_required":
            additional_budget_required,

        "suggestion": (
            f"Increase the budget by "
            f"₹{additional_budget_required:,.2f} "
            f"to purchase the selected product."
        )
    }

    print("\nAlternative Suggestion:")

    for key, value in suggestion.items():

        print(f"{key}: {value}")

    return {

        "alternative_suggestion": suggestion
    }