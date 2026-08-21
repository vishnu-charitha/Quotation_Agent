from backend.nodes.product_search_node import product_search_node


def test_product_search_node():

    state = {
        "customer_name": "ABC Technologies",
        "processor": "i5",
        "ram": "16GB",
        "storage": "512GB SSD",
        "quantity": 15,
        "max_budget": 65000
    }

    result = product_search_node(state)

    print("\nMatching Products:")

    for product in result["matching_products"]:
        print(
            f"{product['brand']} "
            f"{product['model']} "
            f"- ₹{product['supplier_price']}"
        )

    print("\nRanked Products:")

    for product in result["ranked_products"]:
        print(
            f"{product['brand']} "
            f"{product['model']} "
            f"- ₹{product['supplier_price']}"
        )

    print("\nSelected Product:")

    selected = result["selected_product"]

    print(
        f"{selected['brand']} "
        f"{selected['model']}"
    )

    assert result["selected_product"] is not None
    assert result["error"] is None