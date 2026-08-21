def product_search_node(state):

    print("\n--- PRODUCT SEARCH NODE ---")

    requirements = state["requirements"]

    print("\nCustomer Requirements:")
    print(requirements)

    print("\nSearching products based on requirements...")


    # --------------------------------
    # PRODUCT DATABASE
    # --------------------------------

    products = [

        {
            "product_id": "L001",
            "supplier": "Tech Supplier A",
            "brand": "Lenovo",
            "model": "IdeaPad Slim 5",
            "processor": "Intel Core i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "price": 50000,
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
            "price": 52000,
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
            "price": 48500,
            "warranty": "2 Years"
        },

        {
            "product_id": "L004",
            "supplier": "Tech Supplier A",
            "brand": "Lenovo",
            "model": "ThinkPad E14",
            "processor": "Intel Core i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "price": 65000,
            "warranty": "1 Year"
        },

        {
            "product_id": "L005",
            "supplier": "Tech Supplier B",
            "brand": "HP",
            "model": "Victus",
            "processor": "Intel Core i7",
            "ram": "16GB",
            "storage": "1TB SSD",
            "price": 70000,
            "warranty": "1 Year"
        }
    ]


    # --------------------------------
    # FILTER MATCHING PRODUCTS
    # --------------------------------

    matching_products = []

    for product in products:

        if (
            requirements["processor"].lower()
            in product["processor"].lower()

            and requirements["ram"].lower()
            == product["ram"].lower()

            and requirements["storage"].lower()
            == product["storage"].lower()

            and product["price"]
            <= requirements["max_budget"]
        ):

            matching_products.append(product)


    # --------------------------------
    # NO PRODUCT FOUND
    # --------------------------------

    if not matching_products:

        raise ValueError(
            "No products found matching the customer requirements"
        )


    # --------------------------------
    # SORT BY PRICE
    # --------------------------------

    matching_products.sort(
        key=lambda product: product["price"]
    )


    # --------------------------------
    # SELECT BEST PRODUCT
    # --------------------------------

    selected_product = matching_products[0]


    print("\nMatching Products:")

    for product in matching_products:

        print(
            f"{product['brand']} "
            f"{product['model']} | "
            f"{product['supplier']} | "
            f"₹{product['price']}"
        )


    print("\nBest Selected Product:")

    print(selected_product)


    # IMPORTANT:
    # Return all matching products AND selected product

    return {
        "matching_products": matching_products,
        "selected_product": selected_product
    }