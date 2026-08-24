def alternative_product_node(state):

    print("\n==============================")
    print("ALTERNATIVE PRODUCT NODE")
    print("==============================")

    requirements = state["requirements"]

    retrieved_documents = state.get(
        "retrieved_documents",
        []
    )

    current_product = state.get(
        "selected_product",
        {}
    )

    quantity = requirements["quantity"]

    current_product_id = current_product.get(
        "product_id"
    )

    print("\nCurrent Product:")

    print(current_product)

    print(
        "\nSearching for alternative products..."
    )


    # ==========================================
    # EXTRACT PRODUCTS FROM RAG DOCUMENTS
    # ==========================================

    alternative_products = []


    for document in retrieved_documents:

        product = document.get(
            "product"
        )

        if not product:
            continue


        # Skip currently selected product

        if (
            product.get("product_id")
            == current_product_id
        ):

            continue


        # Check quantity availability

        if (
            product.get(
                "available_quantity",
                0
            )
            < quantity
        ):

            continue


        alternative_products.append(
            product
        )


    # ==========================================
    # CHECK ALTERNATIVES
    # ==========================================

    if not alternative_products:

        print(
            "\nNo alternative products found."
        )

        return {

            "alternative_available":
                False
        }


    # ==========================================
    # SELECT NEXT CHEAPEST PRODUCT
    # ==========================================

    alternative_products = sorted(

        alternative_products,

        key=lambda product:
        product["supplier_price"]
    )


    selected_product = alternative_products[0]


    print("\nAlternative Product Selected:")

    print(selected_product)


    return {

        "selected_product":
            selected_product,

        "alternative_available":
            True
    }