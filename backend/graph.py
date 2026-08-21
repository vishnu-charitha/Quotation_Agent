from langgraph.graph import StateGraph, START, END

from backend.state import QuotationState

from backend.nodes.requirement_node import requirement_node
from backend.nodes.product_search_node import product_search_node
from backend.nodes.pricing_node import pricing_node
from backend.nodes.quotation_node import quotation_node
from backend.nodes.approval_node import approval_node


def create_quotation_graph():

    workflow = StateGraph(QuotationState)

    # Add nodes
    workflow.add_node("requirements", requirement_node)
    workflow.add_node("product_search", product_search_node)
    workflow.add_node("pricing", pricing_node)
    workflow.add_node("quotation", quotation_node)
    workflow.add_node("approval", approval_node)

    # Add workflow edges
    workflow.add_edge(START, "requirements")

    workflow.add_edge("requirements", "product_search")

    workflow.add_edge("product_search", "pricing")

    workflow.add_edge("pricing", "quotation")

    workflow.add_edge("quotation", "approval")

    workflow.add_edge("approval", END)

    # Compile graph
    graph = workflow.compile()

    return graph