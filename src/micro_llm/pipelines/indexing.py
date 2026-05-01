from micro_llm.scripts.chunker import chunk_documents
from micro_llm.scripts.load import get_documents
from micro_llm.scripts.embed import embed_chunks
from omegaconf import DictConfig


class Indexing:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg.indexing

    def fire(self):
        if self.cfg.pipeline != "enable":
            print("Indexing Pipeline Ignored..")
        else:
            print("Indexing Pipeline Selected..")
            documents_loaded = get_documents(cfg=self.cfg)
            chunks_loaded = chunk_documents(docs=documents_loaded, cfg=self.cfg)
            embed_chunks(chunks=chunks_loaded, cfg=self.cfg)
