from backend.tools.quotation_generator import (
    generate_quotation_pdf
)


def pdf_node(state):

    print("\n==============================")
    print("PDF GENERATION NODE")
    print("==============================")

    quotation = state["quotation"]

    pdf_path = generate_quotation_pdf(
        quotation
    )

    print(
        "\nPDF Generated Successfully"
    )

    print(
        f"PDF Path: {pdf_path}"
    )

    return {
        "pdf_path": pdf_path
    }