from backend.services.pricing_service import calculate_price


def test_calculate_price():

    result = calculate_price(
        supplier_price=58000,
        quantity=15,
        profit_margin=10,
        gst_rate=18
    )

    print("\nPricing Details:")

    for key, value in result.items():
        print(f"{key}: {value}")

    assert result["selling_price_per_unit"] == 63800
    assert result["final_total"] == 1129260