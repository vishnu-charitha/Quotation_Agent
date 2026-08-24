import re


def requirement_node(state):

    print("\n==============================")
    print("REQUIREMENT NODE")
    print("==============================")

    query = state["query"]

    print("\nCustomer Query:")
    print(query)

    # ==========================================
    # EXTRACT CUSTOMER NAME
    # ==========================================

    name_match = re.search(
        r"(?:my name is|name is|i am)\s+([A-Za-z]+)",
        query,
        re.IGNORECASE
    )

    customer_name = (
        name_match.group(1)
        if name_match
        else "Customer"
    )

    # ==========================================
    # EXTRACT PROCESSOR
    # ==========================================

    processor_match = re.search(
        r"(Intel\s+Core\s+i[3579]|AMD\s+Ryzen\s+[3579])",
        query,
        re.IGNORECASE
    )

    processor = (
        processor_match.group(1)
        if processor_match
        else None
    )

    # ==========================================
    # EXTRACT RAM
    # ==========================================

    ram_match = re.search(
        r"(\d+\s*GB)\s*RAM",
        query,
        re.IGNORECASE
    )

    ram = (
        ram_match.group(1).replace(" ", "")
        if ram_match
        else None
    )

    # ==========================================
    # EXTRACT STORAGE
    # ==========================================

    storage_match = re.search(
        r"(\d+\s*(?:GB|TB)\s*(?:SSD|HDD))",
        query,
        re.IGNORECASE
    )

    storage = (
        storage_match.group(1)
        if storage_match
        else None
    )

    # ==========================================
    # EXTRACT QUANTITY
    # ==========================================

    quantity_match = re.search(
        r"(\d+)\s*laptops?",
        query,
        re.IGNORECASE
    )

    quantity = (
        int(quantity_match.group(1))
        if quantity_match
        else None
    )

    # ==========================================
    # EXTRACT MAXIMUM BUDGET
    # ==========================================

    budget_match = re.search(
        r"(?:maximum budget is|budget is|budget)\s*(?:₹|Rs\.?)?\s*(\d+)",
        query,
        re.IGNORECASE
    )

    max_budget = (
        float(budget_match.group(1))
        if budget_match
        else None
    )

    # ==========================================
    # CREATE REQUIREMENTS
    # ==========================================

    requirements = {
        "customer_name": customer_name,
        "processor": processor,
        "ram": ram,
        "storage": storage,
        "quantity": quantity,
        "max_budget": max_budget
    }

    print("\nExtracted Requirements:")

    for key, value in requirements.items():

        print(f"{key}: {value}")

    # ==========================================
    # VALIDATE REQUIREMENTS
    # ==========================================

    missing_fields = []

    for key, value in requirements.items():

        if value is None:

            missing_fields.append(key)

    if missing_fields:

        raise ValueError(
            "Could not extract the following information "
            f"from the query: {', '.join(missing_fields)}"
        )

    return {
        "customer_name": customer_name,
        "requirements": requirements
    }