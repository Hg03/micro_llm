from micro_llm.scripts.retrieve import get_relevant_docs, format_retrieved_context
from micro_llm.scripts.generator import generate_rag_answer
from omegaconf import DictConfig


class Inference:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg.inference

    def fire(self, query: str) -> dict:
        print("Inference Pipeline Started..")
        relevant_docs = get_relevant_docs(query=query, cfg=self.cfg)
        formatted_context = format_retrieved_context(points=relevant_docs)
        answer = generate_rag_answer(
            query=query, context=formatted_context, cfg=self.cfg
        )
        sources = list({p.payload["source"] for p in relevant_docs})
        return {"answer": answer, "sources": sources}
