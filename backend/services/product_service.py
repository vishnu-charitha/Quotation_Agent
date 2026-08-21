from backend.services.dataset_service import load_laptops


def search_laptops(
    processor=None,
    ram=None,
    storage=None,
    quantity=None,
    max_budget=None
):
    laptops = load_laptops()

    matching_laptops = []

    for laptop in laptops:

        processor_match = (
            processor is None
            or processor.lower() in laptop["processor"].lower()
        )

        ram_match = (
            ram is None
            or ram.lower() == laptop["ram"].lower()
        )

        storage_match = (
            storage is None
            or storage.lower() == laptop["storage"].lower()
        )

        quantity_match = (
            quantity is None
            or int(laptop["available_quantity"]) >= quantity
        )

        budget_match = (
            max_budget is None
            or float(laptop["market_price"]) <= max_budget
        )

        availability_match = (
            laptop["availability"].lower() == "in stock"
        )

        if (
            processor_match
            and ram_match
            and storage_match
            and quantity_match
            and budget_match
            and availability_match
        ):
            matching_laptops.append(laptop)

    return matching_laptops