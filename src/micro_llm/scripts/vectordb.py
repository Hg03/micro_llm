from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from omegaconf import DictConfig
from dotenv import load_dotenv
import os

load_dotenv()


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=os.getenv("QDRANT_CLUSTER_ENDPOINT"),
        api_key=os.getenv("QDRANT_API_KEY"),
        cloud_inference=True,
    )


def ensure_collection(client: QdrantClient, cfg: DictConfig, vector_size: int) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if cfg.embed.collection_name not in existing:
        client.create_collection(
            collection_name=cfg.embed.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        print(f"Created collection: {cfg.embed.collection_name}")
