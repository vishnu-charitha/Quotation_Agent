import json
from pathlib import Path

from backend.rag.document_loader import load_all_documents
from backend.rag.text_splitter import split_documents
from langchain_huggingface import HuggingFaceEmbeddings


def export_chunks_and_embeddings():

    # ==========================================
    # PROJECT PATH
    # ==========================================

    BASE_DIR = Path(__file__).resolve().parents[2]

    CHUNKS_FILE = BASE_DIR / "chunks.txt"

    EMBEDDINGS_FILE = BASE_DIR / "embeddings.json"


    # ==========================================
    # STEP 1: LOAD DOCUMENTS
    # ==========================================

    print("\nLoading documents...")

    documents = load_all_documents()


    # ==========================================
    # STEP 2: CREATE CHUNKS
    # ==========================================

    print("\nCreating chunks...")

    chunks = split_documents(documents)

    print(f"\nTotal chunks: {len(chunks)}")


    # ==========================================
    # STEP 3: SAVE CHUNKS
    # ==========================================

    print("\nSaving chunks...")

    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:

        for i, chunk in enumerate(chunks, start=1):

            file.write("=" * 60 + "\n")

            file.write(f"CHUNK {i}\n")

            file.write("=" * 60 + "\n\n")

            file.write(chunk.page_content + "\n\n")

            file.write("METADATA:\n")

            file.write(
                json.dumps(
                    chunk.metadata,
                    indent=4,
                    default=str
                )
            )

            file.write("\n\n")


    print("Chunks saved successfully!")


    # ==========================================
    # STEP 4: LOAD EMBEDDING MODEL
    # ==========================================

    print("\nLoading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    # ==========================================
    # STEP 5: CREATE EMBEDDINGS
    # ==========================================

    embeddings_data = []

    for i, chunk in enumerate(chunks, start=1):

        print(f"Generating embedding for chunk {i}...")

        vector = embedding_model.embed_query(
            chunk.page_content
        )

        embeddings_data.append(
            {
                "chunk_number": i,
                "chunk_text": chunk.page_content,
                "metadata": chunk.metadata,
                "embedding": vector,
                "dimensions": len(vector)
            }
        )


    # ==========================================
    # STEP 6: SAVE EMBEDDINGS
    # ==========================================

    print("\nSaving embeddings...")

    with open(
        EMBEDDINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            embeddings_data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )


    # ==========================================
    # VERIFY FILES
    # ==========================================

    print("\n================================")
    print("EXPORT COMPLETED SUCCESSFULLY")
    print("================================")

    print(f"\nChunks File:")
    print(CHUNKS_FILE)

    print(f"File size: {CHUNKS_FILE.stat().st_size} bytes")

    print(f"\nEmbeddings File:")
    print(EMBEDDINGS_FILE)

    print(
        f"File size: "
        f"{EMBEDDINGS_FILE.stat().st_size} bytes"
    )


if __name__ == "__main__":
    export_chunks_and_embeddings()