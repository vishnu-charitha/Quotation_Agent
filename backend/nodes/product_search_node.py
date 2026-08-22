from backend.tools.supplier_tool import search_suppliers


def product_search_node(state):

    print("\n--- PRODUCT SEARCH NODE ---")

    requirements = state["requirements"]

    products = search_suppliers(
        requirements["processor"],
        requirements["ram"],
        requirements["storage"]
    )

    if not products:
        raise ValueError("No matching products found")

    quantity = requirements["quantity"]

    available_products = [
        product
        for product in products
        if product.get("available_quantity", 100) >= quantity
    ]

    if not available_products:
        available_products = products

    selected_product = min(
        available_products,
        key=lambda x: x["supplier_price"]
    )

    print("\nSelected Product:")
    print(selected_product)

    return {
        "selected_product": selected_product
    }