from langgraph.graph import StateGraph, END

from backend.state import QuotationState

from backend.nodes.requirement_node import requirement_node
from backend.nodes.rag_retrieval_node import rag_retrieval_node
from backend.nodes.product_search_node import product_search_node
from backend.nodes.pricing_node import pricing_node
from backend.nodes.approval_node import approval_node
from backend.nodes.quotation_node import quotation_node
from backend.nodes.pdf_node import pdf_node


# =========================================================
# APPROVAL ROUTER
# =========================================================

def approval_router(state: QuotationState):

    print("\n==============================")
    print("APPROVAL ROUTER")
    print("==============================")

    approval_status = state.get(
        "approval_status",
        "PENDING"
    )

    print(
        f"Approval Status: {approval_status}"
    )


    # -----------------------------------------------------
    # APPROVED
    # -----------------------------------------------------

    if approval_status == "APPROVED":

        print(
            "Quotation approved. "
            "Proceeding to quotation generation."
        )

        return "quotation"


    # -----------------------------------------------------
    # PENDING
    # -----------------------------------------------------

    elif approval_status == "PENDING":

        print(
            "Quotation is pending approval."
        )

        return END


    # -----------------------------------------------------
    # REJECTED
    # -----------------------------------------------------

    elif approval_status == "REJECTED":

        print(
            "Quotation rejected."
        )

        return END


    # -----------------------------------------------------
    # UNKNOWN STATUS
    # -----------------------------------------------------

    else:

        print(
            f"Unknown approval status: "
            f"{approval_status}"
        )

        return END


# =========================================================
# CREATE WORKFLOW
# =========================================================

workflow = StateGraph(
    QuotationState
)


# =========================================================
# ADD NODES
# =========================================================

workflow.add_node(
    "requirements",
    requirement_node
)

workflow.add_node(
    "rag_retrieval",
    rag_retrieval_node
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
    "approval",
    approval_node
)

workflow.add_node(
    "quotation",
    quotation_node
)

workflow.add_node(
    "pdf",
    pdf_node
)


# =========================================================
# SET ENTRY POINT
# =========================================================

workflow.set_entry_point(
    "requirements"
)


# =========================================================
# ADD NORMAL EDGES
# =========================================================

workflow.add_edge(
    "requirements",
    "rag_retrieval"
)

workflow.add_edge(
    "rag_retrieval",
    "product_search"
)

workflow.add_edge(
    "product_search",
    "pricing"
)

workflow.add_edge(
    "pricing",
    "approval"
)


# =========================================================
# CONDITIONAL APPROVAL ROUTING
# =========================================================

workflow.add_conditional_edges(
    "approval",
    approval_router,
    {
        "quotation": "quotation",
        END: END
    }
)


# =========================================================
# FINAL QUOTATION FLOW
# =========================================================

workflow.add_edge(
    "quotation",
    "pdf"
)

workflow.add_edge(
    "pdf",
    END
)


# =========================================================
# COMPILE GRAPH
# =========================================================

quotation_graph = workflow.compile()