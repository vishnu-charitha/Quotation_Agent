from langgraph.graph import StateGraph, START, END

from backend.state import QuotationState

from backend.nodes.requirement_node import requirement_node
from backend.nodes.product_search_node import product_search_node
from backend.nodes.pricing_node import pricing_node
from backend.nodes.quotation_node import quotation_node
from backend.nodes.approval_node import approval_node

from backend.nodes.auto_approval_node import auto_approval_node
from backend.nodes.manual_approval_node import manual_approval_node


def approval_decision(state):

    print("\n--- APPROVAL DECISION ---")

    pricing_details = state["pricing_details"]

    final_total = pricing_details["final_total"]

    print(f"Final Total: ₹{final_total}")

    if final_total <= 1000000:

        print("Decision: AUTO APPROVE")

        return "auto_approve"

    else:

        print("Decision: MANUAL APPROVAL")

        return "manual_approve"


def create_quotation_graph():

    workflow = StateGraph(QuotationState)

    # Add nodes
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
        "auto_approve",
        auto_approval_node
    )

    workflow.add_node(
        "manual_approval",
        manual_approval_node
    )

    # START → Requirements
    workflow.add_edge(
        START,
        "requirements"
    )

    # Requirements → Product Search
    workflow.add_edge(
        "requirements",
        "product_search"
    )

    # Product Search → Pricing
    workflow.add_edge(
        "product_search",
        "pricing"
    )

    # Pricing → Quotation
    workflow.add_edge(
        "pricing",
        "quotation"
    )

    # Quotation → Approval
    workflow.add_edge(
        "quotation",
        "approval"
    )

    # Conditional routing
    workflow.add_conditional_edges(
        "approval",
        approval_decision,
        {
            "auto_approve": "auto_approve",
            "manual_approve": "manual_approval"
        }
    )

    # End both paths
    workflow.add_edge(
        "auto_approve",
        END
    )

    workflow.add_edge(
        "manual_approval",
        END
    )

    # Compile graph
    graph = workflow.compile()

    return graph