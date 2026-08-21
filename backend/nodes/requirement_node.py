def requirement_node(state):

    print("\n--- REQUIREMENT NODE ---")

    requirements = state["requirements"]

    print("\nCustomer Requirements:")

    for key, value in requirements.items():
        print(f"{key}: {value}")

    return {
        "customer_name": state["customer_name"],
        "requirements": requirements
    }