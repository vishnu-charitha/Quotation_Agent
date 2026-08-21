from backend.services.product_service import search_laptops, rank_laptops
from backend.services.pricing_service import calculate_price


def test_product_search_and_pricing():

    # Step 1: Search for matching laptops
    laptops = search_laptops(
        processor="i5",
        ram="16GB",
        storage="512GB SSD",
        quantity=15,
        max_budget=65000
    )

    assert len(laptops) > 0

    print("\nMatching Products:")

    for laptop in laptops:
        print(
            f"{laptop['brand']} {laptop['model']} - "
            f"Supplier Price: ₹{laptop['supplier_price']}"
        )

    # Step 2: Rank matching laptops by supplier price
    ranked_laptops = rank_laptops(laptops)

    print("\nRanked Products:")

    for laptop in ranked_laptops:
        print(
            f"{laptop['brand']} {laptop['model']} - "
            f"Supplier Price: ₹{laptop['supplier_price']}"
        )

    # Step 3: Select the best-ranked laptop
    selected_laptop = ranked_laptops[0]

    print("\nSelected Product:")
    print(
        f"{selected_laptop['brand']} "
        f"{selected_laptop['model']}"
    )

    # Step 4: Calculate quotation price
    quotation = calculate_price(
        supplier_price=selected_laptop["supplier_price"],
        quantity=15,
        profit_margin=10,
        gst_rate=18
    )

    print("\nQuotation Details:")

    for key, value in quotation.items():
        print(f"{key}: {value}")

    assert quotation["final_total"] > 0