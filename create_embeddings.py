from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).parent
DOCUMENTS_DIR = BASE_DIR / "documents"
EMBEDDINGS_DIR = BASE_DIR / "Embeddings"

EMBEDDINGS_DIR.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

files = [
    path for path in DOCUMENTS_DIR.rglob("*")
    if path.is_file() and path.suffix.lower() in {".txt", ".md", ".pdf"}
]

texts = []
metadata = []

for file in files:
    if file.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        text = "\n".join(page.extract_text() or "" for page in PdfReader(file).pages)
    else:
        text = file.read_text(encoding="utf-8", errors="ignore")

    if text.strip():
        texts.append(text)
        metadata.append({"file": str(file.relative_to(BASE_DIR))})

embeddings = model.encode(texts, normalize_embeddings=True)

np.save(EMBEDDINGS_DIR / "embeddings.npy", embeddings)
(EMBEDDINGS_DIR / "metadata.json").write_text(
    json.dumps(metadata, indent=2),
    encoding="utf-8",
)

print(f"Created {len(embeddings)} embeddings in {EMBEDDINGS_DIR}")