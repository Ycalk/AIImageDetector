import kagglehub.config
from .config import Config
from .dataset import ArtiFactDataset

kagglehub.config.set_kaggle_credentials(Config.KAGGLE_USERNAME, Config.KAGGLE_KEY)


__all__ = [
    "ArtiFactDataset",
]
