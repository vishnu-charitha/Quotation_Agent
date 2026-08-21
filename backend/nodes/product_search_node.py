from backend.state import QuotationState
from backend.services.product_service import (
    search_laptops,
    rank_laptops
)


def product_search_node(state: QuotationState):

    try:

        matching_products = search_laptops(
            processor=state.get("processor"),
            ram=state.get("ram"),
            storage=state.get("storage"),
            quantity=state.get("quantity"),
            max_budget=state.get("max_budget")
        )

        if not matching_products:
            return {
                "matching_products": [],
                "ranked_products": [],
                "selected_product": None,
                "error": "No matching products found."
            }

        ranked_products = rank_laptops(
            matching_products
        )

        selected_product = ranked_products[0]

        return {
            "matching_products": matching_products,
            "ranked_products": ranked_products,
            "selected_product": selected_product,
            "error": None
        }

    except Exception as e:

        return {
            "matching_products": [],
            "ranked_products": [],
            "selected_product": None,
            "error": str(e)
        }