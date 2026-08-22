def search_suppliers(processor, ram, storage):

    suppliers = [
        {
            "product_id": "L001",
            "supplier": "Tech Supplier A",
            "brand": "Lenovo",
            "model": "IdeaPad Slim 5",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "supplier_price": 50000,
            "warranty": "1 Year"
        },
        {
            "product_id": "L002",
            "supplier": "Tech Supplier B",
            "brand": "HP",
            "model": "Pavilion 15",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "supplier_price": 52000,
            "warranty": "1 Year"
        },
        {
            "product_id": "L003",
            "supplier": "Tech Supplier C",
            "brand": "Dell",
            "model": "Inspiron 15",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "supplier_price": 51000,
            "warranty": "1 Year"
        }
    ]

    matching_products = []

    for product in suppliers:

        if (
            processor.lower() in product["processor"].lower()
            and ram.lower() == product["ram"].lower()
            and storage.lower() == product["storage"].lower()
        ):
            matching_products.append(product)

    return matching_products