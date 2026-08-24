from typing import Dict, Any, List


# =========================================================
# CALCULATE ESTIMATED FINAL TOTAL
# =========================================================

def calculate_estimated_total(
    supplier_price: float,
    quantity: int,
    profit_margin_percent: float = 10,
    gst_rate: float = 18
) -> float:

    # Profit amount per unit

    profit_amount = (
        supplier_price
        * profit_margin_percent
        / 100
    )


    # Selling price per unit

    selling_price = (
        supplier_price
        + profit_amount
    )


    # Subtotal

    subtotal = (
        selling_price
        * quantity
    )


    # GST amount

    gst_amount = (
        subtotal
        * gst_rate
        / 100
    )


    # Final total

    final_total = (
        subtotal
        + gst_amount
    )


    return round(
        final_total,
        2
    )


# =========================================================
# EXTRACT PRODUCTS FROM RAG DOCUMENTS
# =========================================================

def extract_products_from_documents(
    documents: List[Dict[str, Any]]
):

    products = []


    for document in documents:

        content = document.get(
            "content",
            ""
        )


        # Convert content into lines

        lines = content.splitlines()


        product = {}


        for line in lines:

            if ":" not in line:

                continue


            key, value = line.split(
                ":",
                1
            )


            key = key.strip()

            value = value.strip()


            # Store known fields

            product[key] = value


        # Only add valid products

        if "product_id" in product:

            # Convert numeric values

            if "supplier_price" in product:

                try:

                    product[
                        "supplier_price"
                    ] = float(
                        product[
                            "supplier_price"
                        ]
                    )

                except ValueError:

                    continue


            if "available_quantity" in product:

                try:

                    product[
                        "available_quantity"
                    ] = int(
                        product[
                            "available_quantity"
                        ]
                    )

                except ValueError:

                    product[
                        "available_quantity"
                    ] = 0


            products.append(
                product
            )


    return products


# =========================================================
# PRODUCT SEARCH NODE
# =========================================================

def product_search_node(state):

    print("\n==============================")
    print("PRODUCT SEARCH NODE")
    print("==============================")


    # -----------------------------------------------------
    # GET REQUIREMENTS
    # -----------------------------------------------------

    requirements = state[
        "requirements"
    ]


    processor = requirements.get(
        "processor",
        ""
    )


    ram = requirements.get(
        "ram",
        ""
    )


    storage = requirements.get(
        "storage",
        ""
    )


    quantity = int(
        requirements.get(
            "quantity",
            1
        )
    )


    max_budget = float(
        requirements.get(
            "max_budget",
            0
        )
    )


    print(f"\nQuantity: {quantity}")

    print(
        f"Maximum Budget: {max_budget}"
    )


    # -----------------------------------------------------
    # GET RAG DOCUMENTS
    # -----------------------------------------------------

    retrieved_documents = state.get(
        "retrieved_documents",
        []
    )


    print(
        f"\nInitial Retrieved Documents: "
        f"{len(retrieved_documents)}"
    )


    # -----------------------------------------------------
    # EXTRACT PRODUCTS
    # -----------------------------------------------------

    products = (
        extract_products_from_documents(
            retrieved_documents
        )
    )


    print(
        f"\nProducts extracted initially: "
        f"{len(products)}"
    )


    # -----------------------------------------------------
    # REMOVE DUPLICATE PRODUCTS
    # -----------------------------------------------------

    unique_products = {}


    for product in products:

        product_id = product.get(
            "product_id"
        )


        if product_id:

            unique_products[
                product_id
            ] = product


    products = list(
        unique_products.values()
    )


    # -----------------------------------------------------
    # FIND MATCHING PRODUCTS
    # -----------------------------------------------------

    matching_products = []


    for product in products:

        print(
            "\n--------------------------------"
        )

        print(
            f"Checking Product: "
            f"{product.get('product_id')}"
        )

        print(
            "--------------------------------"
        )


        product_processor = str(
            product.get(
                "processor",
                ""
            )
        )


        product_ram = str(
            product.get(
                "ram",
                ""
            )
        )


        product_storage = str(
            product.get(
                "storage",
                ""
            )
        )


        available_quantity = int(
            product.get(
                "available_quantity",
                0
            )
        )


        print(
            f"Processor: "
            f"{product_processor}"
        )

        print(
            f"RAM: "
            f"{product_ram}"
        )

        print(
            f"Storage: "
            f"{product_storage}"
        )

        print(
            f"Available Quantity: "
            f"{available_quantity}"
        )


        # Check specifications

        specification_match = (

            processor.lower()
            in product_processor.lower()

            and

            ram.lower()
            == product_ram.lower()

            and

            storage.lower()
            == product_storage.lower()

        )


        # Check quantity

        quantity_available = (

            available_quantity
            >= quantity

        )


        if (
            specification_match
            and
            quantity_available
        ):

            print(
                "Result: MATCH FOUND"
            )


            matching_products.append(
                product
            )


        else:

            if not specification_match:

                print(
                    "Result: "
                    "Specification does not match"
                )


            elif not quantity_available:

                print(
                    "Result: "
                    "Insufficient quantity"
                )


    print(
        f"\nMatching Products: "
        f"{len(matching_products)}"
    )


    # -----------------------------------------------------
    # NO MATCHING PRODUCT
    # -----------------------------------------------------

    if not matching_products:

        return {

            "approval_status":
                "REJECTED",

            "rejection_reason":
                (
                    "No products found matching "
                    "the requested specifications "
                    "and quantity."
                )

        }


    # -----------------------------------------------------
    # BUDGET ANALYSIS
    # -----------------------------------------------------

    print(
        "\n=============================="
    )

    print(
        "PRODUCT BUDGET ANALYSIS"
    )

    print(
        "=============================="
    )


    budget_products = []


    for product in matching_products:

        supplier_price = float(
            product[
                "supplier_price"
            ]
        )


        estimated_final_total = (
            calculate_estimated_total(
                supplier_price=
                    supplier_price,

                quantity=
                    quantity
            )
        )


        product[
            "estimated_final_total"
        ] = estimated_final_total


        print(
            f"\nProduct: "
            f"{product.get('product_id')}"
        )

        print(
            f"Supplier Price: "
            f"{supplier_price}"
        )

        print(
            f"Estimated Final Total: "
            f"{estimated_final_total}"
        )

        print(
            f"Maximum Budget: "
            f"{max_budget}"
        )


        if (
            estimated_final_total
            <= max_budget
        ):

            print(
                "Status: WITHIN BUDGET"
            )


            budget_products.append(
                product
            )


        else:

            print(
                "Status: EXCEEDS BUDGET"
            )


    # -----------------------------------------------------
    # NO PRODUCT WITHIN BUDGET
    # -----------------------------------------------------

    if not budget_products:

        cheapest_product = min(

            matching_products,

            key=lambda product:
            product[
                "estimated_final_total"
            ]

        )


        print(
            "\nNo matching product fits "
            "within the customer's budget."
        )


        print(
            f"\nCheapest Available Product: "
            f"{cheapest_product.get('product_id')}"
        )


        print(
            f"Cheapest Final Total: "
            f"{cheapest_product.get('estimated_final_total')}"
        )


        return {

            "selected_product":
                cheapest_product,

            "approval_status":
                "REJECTED",

            "rejection_reason":
                (
                    f"No matching product fits "
                    f"within the maximum budget "
                    f"of ₹{max_budget}. "
                    f"The cheapest available option "
                    f"costs ₹"
                    f"{cheapest_product.get('estimated_final_total')}."
                )

        }


    # -----------------------------------------------------
    # SELECT CHEAPEST PRODUCT
    # -----------------------------------------------------

    selected_product = min(

        budget_products,

        key=lambda product:
        product[
            "estimated_final_total"
        ]

    )


    print(
        "\n=============================="
    )

    print(
        "SELECTED PRODUCT"
    )

    print(
        "=============================="
    )

    print(
        selected_product
    )


    return {

        "selected_product":
            selected_product,

        "approval_status":
            "PENDING"

    }