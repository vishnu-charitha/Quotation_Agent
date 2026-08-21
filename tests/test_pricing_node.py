from backend.nodes.pricing_node import pricing_node


def test_pricing_node():

    state = {
        "requirements": {
            "quantity": 15
        },

        "selected_product": {
            "brand": "Lenovo",
            "model": "ThinkPad E14",
            "supplier_price": "57000"
        }
    }

    result = pricing_node(state)

    print("\nPricing Node Result:")

    for key, value in result["pricing_details"].items():
        print(f"{key}: {value}")

    assert result["pricing_details"]["final_total"] > 0