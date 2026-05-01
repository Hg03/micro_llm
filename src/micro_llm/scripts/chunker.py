from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from micro_llm.scripts.utils import Document, Chunk
from docling.chunking import HybridChunker
from transformers import AutoTokenizer
from omegaconf import DictConfig
from typing import List


def chunk_documents(docs: List[Document], cfg: DictConfig):
    tokenizer = HuggingFaceTokenizer(tokenizer=AutoTokenizer.from_pretrained(cfg.model))
    chunker = HybridChunker(tokenizer=tokenizer, max_tokens=cfg.chunker.max_tokens)
    chunks = []
    for doc in docs:
        splits = chunker.chunk(doc.content)
        for i, split in enumerate(splits):
            chunks.append(
                Chunk(
                    content=chunker.contextualize(split),
                    chunk_id=f"{doc.doc_id}_chunk_{i}",
                    doc_id=doc.doc_id,
                    source=doc.source,
                )
            )
    print(f"Created {len(chunks)} chunks from {len(docs)} documents")
    return chunks
