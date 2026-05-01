from micro_llm.pipelines.indexing import Indexing
from omegaconf import DictConfig
import hydra


@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    Indexing(cfg=cfg).fire()


if __name__ == "__main__":
    main()
