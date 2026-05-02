index:
    @echo "Running Indexing Pipeline"
    @python src/micro_llm/entrypoints/indexing_endpoint.py

infer:
    @echo "Running Inference Pipeline"
    @uv run uvicorn micro_llm.entrypoints.inference_endpoint:app --host 0.0.0.0 --port 8001 --reload