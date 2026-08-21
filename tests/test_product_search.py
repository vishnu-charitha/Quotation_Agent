from backend.services.product_service import search_laptops


def test_search_laptops():
    laptops = search_laptops(
        processor="i5",
        ram="16GB",
        storage="512GB SSD",
        quantity=15,
        max_budget=65000
    )

    print("\nMatching laptops:")

    for laptop in laptops:
        print(
            f"{laptop['brand']} {laptop['model']} - "
            f"{laptop['processor']}, "
            f"{laptop['ram']}, "
            f"{laptop['storage']} | "
            f"Available: {laptop['available_quantity']} | "
            f"Market Price: ₹{laptop['market_price']}"
        )

    assert len(laptops) == 2