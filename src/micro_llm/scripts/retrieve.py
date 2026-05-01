from micro_llm.scripts.vectordb import get_qdrant_client
from micro_llm.scripts.embed import get_embedder
from qdrant_client.models import QueryResponse
from omegaconf import DictConfig
from typing import List


# def embed_query(query: str, client: QdrantClient, model: str, collection_name: str):
#     points = [
#         PointStruct(id=str(uuid.uuid4()), vector=Document(text=query, model=model))
#     ]
#     client.upsert(collection_name=collection_name, points=points)


def get_relevant_docs(cfg: DictConfig) -> List[QueryResponse]:
    embedder = get_embedder(cfg=cfg)
    client = get_qdrant_client()
    query_vector = embedder.embed_query(cfg.retrieve.query)

    # Search Qdrant with the raw vector
    results = client.query_points(
        collection_name=cfg.retrieve.collection_name,
        query=query_vector,
        limit=cfg.retrieve.top_k,
    )
    return results.points


def format_retrieved_context(points) -> list[str]:
    return [p.payload["content"] for p in points if p.payload.get("content")]
