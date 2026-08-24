def pricing_node(state):

    print("\n==============================")
    print("PRICING NODE")
    print("==============================")


    selected_product = state[
        "selected_product"
    ]


    requirements = state[
        "requirements"
    ]


    supplier_price = float(
        selected_product[
            "supplier_price"
        ]
    )


    quantity = int(
        requirements[
            "quantity"
        ]
    )


    # Profit Margin

    profit_margin_percent = 10


    profit_amount_per_unit = (

        supplier_price
        * profit_margin_percent
        / 100

    )


    selling_price_per_unit = (

        supplier_price
        + profit_amount_per_unit

    )


    # Subtotal

    subtotal = (

        selling_price_per_unit
        * quantity

    )


    # GST

    gst_rate = 18


    gst_amount = (

        subtotal
        * gst_rate
        / 100

    )


    # Final Total

    final_total = (

        subtotal
        + gst_amount

    )


    pricing_details = {

        "supplier_price_per_unit":
            round(
                supplier_price,
                2
            ),

        "quantity":
            quantity,

        "profit_margin_percent":
            profit_margin_percent,

        "profit_amount_per_unit":
            round(
                profit_amount_per_unit,
                2
            ),

        "selling_price_per_unit":
            round(
                selling_price_per_unit,
                2
            ),

        "subtotal":
            round(
                subtotal,
                2
            ),

        "gst_rate":
            gst_rate,

        "gst_amount":
            round(
                gst_amount,
                2
            ),

        "final_total":
            round(
                final_total,
                2
            )

    }


    print("\nPricing Details:")


    for key, value in pricing_details.items():

        print(
            f"{key}: {value}"
        )


    return {

        "pricing_details":
            pricing_details

    }