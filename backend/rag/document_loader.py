from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader
)


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DATASETS_DIR = BASE_DIR / "datasets"


# ==========================================
# LOAD TXT FILES
# ==========================================

def load_text_documents():

    documents = []

    text_files = [

        DATA_DIR / "company_policy.txt",

        DATA_DIR / "pricing_policy.txt",

        DATA_DIR / "supplier_catalog.txt"

    ]

    for file_path in text_files:

        if file_path.exists():

            loader = TextLoader(
                str(file_path),
                encoding="utf-8"
            )

            docs = loader.load()

            documents.extend(docs)

            print(
                f"Loaded text file: "
                f"{file_path.name}"
            )

        else:

            print(
                f"File not found: "
                f"{file_path}"
            )

    return documents


# ==========================================
# LOAD CSV FILES
# ==========================================

def load_csv_documents():

    documents = []

    csv_files = [

        DATA_DIR / "products.csv",

        DATASETS_DIR / "laptops.csv",

        DATASETS_DIR / "desktops.csv",

        DATASETS_DIR / "printers.csv",

        DATASETS_DIR / "networking_equipment.csv"

    ]

    for file_path in csv_files:

        if file_path.exists():

            loader = CSVLoader(
                file_path=str(file_path),
                encoding="utf-8"
            )

            docs = loader.load()

            documents.extend(docs)

            print(
                f"Loaded CSV file: "
                f"{file_path.name}"
            )

        else:

            print(
                f"File not found: "
                f"{file_path}"
            )

    return documents


# ==========================================
# LOAD ALL DOCUMENTS
# ==========================================

def load_all_documents():

    print("\n==============================")
    print("LOADING DOCUMENTS")
    print("==============================")

    text_documents = load_text_documents()

    csv_documents = load_csv_documents()

    all_documents = (

        text_documents
        + csv_documents

    )

    print(
        f"\nTotal documents loaded: "
        f"{len(all_documents)}"
    )

    return all_documents