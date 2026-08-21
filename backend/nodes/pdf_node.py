from backend.tools.quotation_generator import generate_quotation_pdf


def pdf_node(state):

    print("\n--- PDF GENERATION NODE ---")

    quotation = state["quotation"]

    pdf_path = generate_quotation_pdf(
        quotation
    )

    print(f"\nPDF Generated Successfully:")
    print(pdf_path)

    return {
        "pdf_path": pdf_path
    }