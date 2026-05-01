from micro_llm.pipelines.inference import Inference
from hydra import compose, initialize


def main():

    with initialize(
        config_path="../conf", job_name="inference"
    ):  # adjust path to your conf dir
        cfg = compose(config_name="config")
    artifacts = Inference(cfg).fire()
    print(artifacts)


if __name__ == "__main__":
    main()
