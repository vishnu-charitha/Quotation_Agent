from langchain_core.tools import tool

from backend.rag.retriever import get_rag_context


# =========================================================
# RAG KNOWLEDGE BASE SEARCH TOOL
# =========================================================

@tool
def search_quotation_knowledge_base(query: str) -> str:
    """
    Search the Qdrant knowledge base for supplier information,
    product specifications, prices, warranties, availability,
    pricing policies, and company quotation policies.
    """

    print("\n=================================")
    print("RAG TOOL CALLED")
    print("=================================")

    print(f"Search Query: {query}")

    try:

        context = get_rag_context(
            query=query,
            limit=5
        )

        return context

    except Exception as error:

        return (
            "Error searching the quotation knowledge base: "
            f"{str(error)}"
        )


# =========================================================
# SUPPLIER SEARCH TOOL
# =========================================================

@tool
def supplier_search_tool(
    requirement: str
) -> str:

    print("\n=================================")
    print("SUPPLIER SEARCH TOOL CALLED")
    print("=================================")

    print(f"Requirement: {requirement}")

    return (
        "Supplier search should use the quotation "
        "knowledge base to find matching products. "
        f"Customer requirement: {requirement}"
    )


# =========================================================
# PRICE CALCULATION TOOL
# =========================================================

@tool
def price_calculation_tool(
    price_per_unit: float,
    quantity: int
) -> str:

    total_price = price_per_unit * quantity

    return (
        f"Price Per Unit: ₹{price_per_unit:,.2f}\n"
        f"Quantity: {quantity}\n"
        f"Total Price: ₹{total_price:,.2f}"
    )