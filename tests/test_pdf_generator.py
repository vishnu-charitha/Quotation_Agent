from backend.services.product_service import (
    search_laptops,
    rank_laptops
)

from backend.services.pricing_service import calculate_price

from backend.tools.quotation_generator import (
    generate_quotation,
    generate_quotation_pdf
)


def test_generate_pdf():

    # Step 1: Search matching laptops
    laptops = search_laptops(
        processor="i5",
        ram="16GB",
        storage="512GB SSD",
        quantity=15,
        max_budget=65000
    )

    assert len(laptops) > 0

    # Step 2: Rank laptops
    ranked_laptops = rank_laptops(laptops)

    # Step 3: Select best laptop
    selected_laptop = ranked_laptops[0]

    # Step 4: Calculate quotation pricing
    pricing = calculate_price(
        supplier_price=selected_laptop["supplier_price"],
        quantity=15,
        profit_margin=10,
        gst_rate=18
    )

    # Step 5: Generate quotation data
    quotation = generate_quotation(
        customer_name="ABC Technologies",
        selected_product=selected_laptop,
        pricing_details=pricing,
        validity_days=7
    )

    # Step 6: Generate PDF
    pdf_path = generate_quotation_pdf(quotation)

    print("\nPDF GENERATED SUCCESSFULLY")
    print(f"Location: {pdf_path}")

    assert pdf_path.endswith(".pdf")