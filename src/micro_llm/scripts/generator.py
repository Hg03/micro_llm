from huggingface_hub import InferenceClient
from omegaconf import DictConfig
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()


def generate_rag_answer(query: str, context: List[str], cfg: DictConfig):
    client = InferenceClient(model=cfg.response.model, token=os.getenv("HF_TOKEN"))
    messages = [
        {
            "role": "system",
            "content": "You are a technical expert. Answer the question using ONLY the provided context.",
        },
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"},
    ]

    # This calls the Hugging Face hosted API instead of running it locally
    response = client.chat_completion(
        messages=messages, max_tokens=500, temperature=0.1
    )

    return response.choices[0].message.content
