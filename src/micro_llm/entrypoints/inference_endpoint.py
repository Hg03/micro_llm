from micro_llm.pipelines.inference import Inference
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from hydra import compose, initialize
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
from uuid import uuid4

load_dotenv()

state: dict = {}

# Server stores session histories
sessions: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    with initialize(config_path="../conf", job_name="inference"):
        cfg = compose(config_name="config")
    state["cfg"] = cfg
    yield
    state.clear()


app = FastAPI(title="micro_llm RAG API", lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str
    session_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok" if "cfg" in state else "unavailable"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        session_id = request.session_id or str(uuid4())
        history = sessions.get(session_id, [])
        result = Inference(cfg=state["cfg"]).fire(
            query=request.question, history=history
        )
        # Update session history on server
        sessions[session_id] = [
            *history,
            {"role": "user", "content": request.question},
            {"role": "assistant", "content": result["answer"]},
        ]
        return QueryResponse(
            answer=result["answer"], sources=result["sources"], session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
