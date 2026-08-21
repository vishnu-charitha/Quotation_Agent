def requirement_node(state):

    print("\n--- REQUIREMENT NODE ---")

    requirements = state.get("requirements", {})

    if not requirements:
        raise ValueError("Requirements are missing from the workflow state")

    print("\nCustomer Requirements:")

    for key, value in requirements.items():
        print(f"{key}: {value}")

    return {
        "requirements": requirements
    }