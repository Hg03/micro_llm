from micro_llm.scripts.vectordb import get_qdrant_client, ensure_collection
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from qdrant_client.models import PointStruct
from micro_llm.scripts.chunker import Chunk
from omegaconf import DictConfig
from dotenv import load_dotenv
import uuid

load_dotenv()


def get_embedder(cfg: DictConfig) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=cfg.model)


def embed_chunks(chunks: list[Chunk], cfg: DictConfig) -> None:
    embedder = get_embedder(cfg)
    client = get_qdrant_client()

    texts = [chunk.content for chunk in chunks]
    embeddings = embedder.embed_documents(texts)

    ensure_collection(client, cfg, vector_size=len(embeddings[0]))

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": chunk.content,
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "source": chunk.source,
            },
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.upsert(
        collection_name=cfg.embed.collection_name,
        points=points,
    )

    print(f"Embedded and stored {len(points)} chunks to Qdrant")
