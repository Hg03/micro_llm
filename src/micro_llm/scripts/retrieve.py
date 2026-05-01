from micro_llm.scripts.vectordb import get_qdrant_client
from qdrant_client.models import Document, PointStruct, QueryResponse
from qdrant_client import QdrantClient
from omegaconf import DictConfig
from typing import List
import uuid


def embed_query(query: str, client: QdrantClient, model: str, collection_name: str):
    points = [
        PointStruct(id=str(uuid.uuid4()), vector=Document(text=query, model=model))
    ]
    client.upsert(collection_name=collection_name, points=points)


def get_relevant_docs(cfg: DictConfig) -> List[QueryResponse]:
    client = get_qdrant_client()
    embed_query(
        query=cfg.retrieve.query,
        client=client,
        model=cfg.retrieve.model,
        collection_name=cfg.retrieve.collection_name,
    )
    results = client.query_points(
        collection_name=cfg.retrieve.collection_name,
        query=Document(text=cfg.retrieve.query, model=cfg.retrieve.model),
        limit=cfg.retrieve.top_k,
    )
    return results


def format_retrieved_context(retrieved_context: List[QueryResponse], cfg: DictConfig):
    context_chunks = []
    for point in retrieved_context.points:
        content = point.payload.get("content")
        if content:
            context_chunks.append(content)
    return context_chunks
