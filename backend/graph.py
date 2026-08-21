from langgraph.graph import StateGraph, START, END

from backend.state import QuotationState

from backend.nodes.requirement_node import requirement_node
from backend.nodes.product_search_node import product_search_node
from backend.nodes.pricing_node import pricing_node
from backend.nodes.quotation_node import quotation_node
from backend.nodes.approval_node import approval_node
from backend.nodes.auto_approval_node import auto_approval_node
from backend.nodes.manual_approval_node import manual_approval_node
from backend.nodes.pdf_node import pdf_node


def approval_decision(state):

    print("\n--- APPROVAL DECISION ---")

    approval_status = state.get("approval_status")

    if approval_status == "approved":
        print("Decision: AUTO APPROVE")
        return "auto_approval"

    print("Decision: MANUAL APPROVAL")
    return "manual_approval"


def create_quotation_graph():

    workflow = StateGraph(QuotationState)

    workflow.add_node(
        "requirements",
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

    workflow.add_node(
        "approval",
        approval_node
    )

    workflow.add_node(
        "auto_approval",
        auto_approval_node
    )

    workflow.add_node(
        "manual_approval",
        manual_approval_node
    )

    workflow.add_node(
        "pdf_generation",
        pdf_node
    )

    workflow.add_edge(
        START,
        "requirements"
    )

    workflow.add_edge(
        "requirements",
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
        "approval"
    )

    workflow.add_conditional_edges(
        "approval",
        approval_decision,
        {
            "auto_approval": "auto_approval",
            "manual_approval": "manual_approval"
        }
    )

    workflow.add_edge(
        "auto_approval",
        "pdf_generation"
    )

    workflow.add_edge(
        "manual_approval",
        "pdf_generation"
    )

    workflow.add_edge(
        "pdf_generation",
        END
    )

    return workflow.compile()