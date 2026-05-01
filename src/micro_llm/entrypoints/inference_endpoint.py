from micro_llm.pipelines.inference import Inference
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from hydra import compose, initialize
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

state: dict = {}


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


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok" if "cfg" in state else "unavailable"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        result = Inference(cfg=state["cfg"]).fire(query=request.question)
        return QueryResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
