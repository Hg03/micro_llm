from micro_llm.scripts.retrieve import get_relevant_docs, format_retrieved_context
from micro_llm.scripts.generator import generate_rag_answer
from omegaconf import DictConfig


class Inference:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg.inference

    def fire(self):
        print("Inference Pipeline Started..")
        relevant_docs = get_relevant_docs(cfg=self.cfg)
        formatted_context = format_retrieved_context(points=relevant_docs)
        answer = generate_rag_answer(
            query=self.cfg.retrieve.query, context=formatted_context, cfg=self.cfg
        )
        return answer
