def calculate_price(
    supplier_price,
    quantity,
    profit_margin=10,
    gst_rate=18
):
    """
    Calculate quotation pricing.

    supplier_price: Cost price of one product
    quantity: Number of units required
    profit_margin: Profit percentage
    gst_rate: GST percentage
    """

    supplier_price = float(supplier_price)

    # Calculate profit amount per unit
    profit_amount = supplier_price * (profit_margin / 100)

    # Selling price before GST
    selling_price_per_unit = supplier_price + profit_amount

    # Subtotal before GST
    subtotal = selling_price_per_unit * quantity

    # GST amount
    gst_amount = subtotal * (gst_rate / 100)

    # Final quotation total
    final_total = subtotal + gst_amount

    return {
        "supplier_price_per_unit": supplier_price,
        "quantity": quantity,
        "profit_margin_percent": profit_margin,
        "profit_amount_per_unit": profit_amount,
        "selling_price_per_unit": selling_price_per_unit,
        "subtotal": subtotal,
        "gst_rate": gst_rate,
        "gst_amount": gst_amount,
        "final_total": final_total
    }