from backend.nodes.approval_node import approval_node


def test_approval_node():

    state = {
        "quotation": {
            "quotation_number": "QT-TEST-001",
            "customer_name": "ABC Technologies",
            "pricing_details": {
                "final_total": 1109790.0
            }
        }
    }

    result = approval_node(state)

    print("\nApproval Result:")
    print(result)

    assert result["approval_status"] == "approved"