from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==========================================
# CREATE TEXT SPLITTER
# ==========================================

def split_documents(documents):

    print("\n==============================")
    print("SPLITTING DOCUMENTS INTO CHUNKS")
    print("==============================")

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )


    chunks = text_splitter.split_documents(
        documents
    )


    print(
        f"\nTotal chunks created: "
        f"{len(chunks)}"
    )


    return chunks