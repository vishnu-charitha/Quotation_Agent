def approval_node(state):

    print("\n==============================")
    print("APPROVAL NODE")
    print("==============================")


    # -----------------------------------------------------
    # CHECK PREVIOUS REJECTION
    # -----------------------------------------------------

    existing_status = state.get(
        "approval_status"
    )


    if existing_status == "REJECTED":

        print(
            "\nRequest already rejected."
        )

        print(
            f"Reason: "
            f"{state.get('rejection_reason')}"
        )


        return {

            "approval_status":
                "REJECTED"

        }


    # -----------------------------------------------------
    # GET DATA
    # -----------------------------------------------------

    pricing_details = state[
        "pricing_details"
    ]


    requirements = state[
        "requirements"
    ]


    final_total = float(

        pricing_details[
            "final_total"
        ]

    )


    max_budget = float(

        requirements[
            "max_budget"
        ]

    )


    print(
        f"\nFinal Total: "
        f"{final_total}"
    )


    print(
        f"Maximum Budget: "
        f"{max_budget}"
    )


    # -----------------------------------------------------
    # APPROVAL LOGIC
    # -----------------------------------------------------

    if final_total <= max_budget:

        approval_status = (
            "APPROVED"
        )


    else:

        approval_status = (
            "REJECTED"
        )


    print(
        f"\nApproval Status: "
        f"{approval_status}"
    )


    return {

        "approval_status":
            approval_status

    }