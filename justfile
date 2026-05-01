index:
    @echo "Running Indexing Pipeline"
    @python src/micro_llm/entrypoints/indexing_endpoint.py

infer:
    @echo "Running Inference Pipeline"
    @python src/micro_llm/entrypoints/inference_endpoint.py