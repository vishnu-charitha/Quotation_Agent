from backend.graph import create_quotation_graph


def test_langgraph_workflow():

    graph = create_quotation_graph()

    initial_state = {

        "customer_name": "ABC Technologies",

        "requirements": {
            "processor": "i5",
            "ram": "16GB",
            "storage": "512GB SSD",
            "quantity": 15,
            "max_budget": 65000
        }
    }

    result = graph.invoke(initial_state)

    print("\n==============================")
    print("FINAL LANGGRAPH RESULT")
    print("==============================")

    print("\nCustomer:")
    print(result["customer_name"])

    print("\nSelected Product:")
    print(
        result["selected_product"]["brand"],
        result["selected_product"]["model"]
    )

    print("\nFinal Total:")
    print(
        f"₹{result['pricing_details']['final_total']}"
    )

    print("\nQuotation Number:")
    print(
        result["quotation"]["quotation_number"]
    )

    print("\nApproval Status:")
    print(
        result["approval_status"]
    )

    print("\nPDF Path:")
    print(
        result.get("pdf_path")
    )

    assert result["customer_name"] == "ABC Technologies"

    assert result["selected_product"] is not None

    assert result["pricing_details"] is not None

    assert result["quotation"] is not None

    assert result["approval_status"] is not None