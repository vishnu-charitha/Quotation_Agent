from pathlib import Path

from qdrant_client import QdrantClient


BASE_DIR = Path(__file__).resolve().parent.parent.parent

QDRANT_PATH = BASE_DIR / "qdrant_db"


def get_qdrant_client():

    client = QdrantClient(
        path=str(QDRANT_PATH)
    )

    return client