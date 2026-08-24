from langgraph.graph import StateGraph, END

from backend.state import QuotationState

from backend.nodes.requirement_node import requirement_node
from backend.nodes.product_search_node import product_search_node
from backend.nodes.pricing_node import pricing_node
from backend.nodes.quotation_node import quotation_node


# =========================================================
# CREATE LANGGRAPH WORKFLOW
# =========================================================

workflow = StateGraph(QuotationState)


# =========================================================
# ADD NODES
# =========================================================

workflow.add_node(
    "requirement",
    requirement_node
)

workflow.add_node(
    "product_search",
    product_search_node
)

workflow.add_node(
    "pricing",
    pricing_node
)

workflow.add_node(
    "quotation",
    quotation_node
)


# =========================================================
# SET ENTRY POINT
# =========================================================

workflow.set_entry_point(
    "requirement"
)


# =========================================================
# ADD WORKFLOW EDGES
# =========================================================

workflow.add_edge(
    "requirement",
    "product_search"
)

workflow.add_edge(
    "product_search",
    "pricing"
)

workflow.add_edge(
    "pricing",
    "quotation"
)

workflow.add_edge(
    "quotation",
    END
)


# =========================================================
# COMPILE GRAPH
# =========================================================

quotation_graph = workflow.compile()