def calculate_price(
    supplier_price_per_unit,
    quantity,
    profit_margin_percent=10,
    gst_rate=18
):

    supplier_price_per_unit = float(supplier_price_per_unit)

    profit_amount_per_unit = (
        supplier_price_per_unit
        * profit_margin_percent
        / 100
    )

    selling_price_per_unit = (
        supplier_price_per_unit
        + profit_amount_per_unit
    )

    subtotal = (
        selling_price_per_unit
        * quantity
    )

    gst_amount = (
        subtotal
        * gst_rate
        / 100
    )

    final_total = (
        subtotal
        + gst_amount
    )

    return {
        "supplier_price_per_unit": supplier_price_per_unit,
        "quantity": quantity,
        "profit_margin_percent": profit_margin_percent,
        "profit_amount_per_unit": profit_amount_per_unit,
        "selling_price_per_unit": selling_price_per_unit,
        "subtotal": subtotal,
        "gst_rate": gst_rate,
        "gst_amount": gst_amount,
        "final_total": final_total
    }