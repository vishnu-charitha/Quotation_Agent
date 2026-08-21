from backend.services.product_service import (
    search_laptops,
    rank_laptops
)

from backend.services.pricing_service import calculate_price

from backend.tools.quotation_generator import generate_quotation


def test_generate_quotation():

    # Search matching laptops
    laptops = search_laptops(
        processor="i5",
        ram="16GB",
        storage="512GB SSD",
        quantity=15,
        max_budget=65000
    )

    # Rank laptops
    ranked_laptops = rank_laptops(laptops)

    # Select the best laptop
    selected_laptop = ranked_laptops[0]

    # Calculate quotation pricing
    pricing = calculate_price(
        supplier_price=selected_laptop["supplier_price"],
        quantity=15,
        profit_margin=10,
        gst_rate=18
    )

    # Generate quotation
    quotation = generate_quotation(
        customer_name="ABC Technologies",
        selected_product=selected_laptop,
        pricing_details=pricing,
        validity_days=7
    )

    print("\nGENERATED QUOTATION\n")

    print(f"Quotation Number: {quotation['quotation_number']}")
    print(f"Quotation Date: {quotation['quotation_date']}")
    print(f"Valid Until: {quotation['valid_until']}")
    print(f"Customer: {quotation['customer_name']}")

    print("\nProduct Details:")

    for key, value in quotation["product"].items():
        print(f"{key}: {value}")

    print("\nPricing Details:")

    for key, value in quotation["pricing"].items():
        print(f"{key}: {value}")

    print(f"\nStatus: {quotation['status']}")

    assert quotation["status"] == "Generated"
    assert quotation["pricing"]["final_total"] > 0