"""Central filesystem paths used throughout the project."""

from pathlib import Path


PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

HISTORICAL_DATA_PATH: Path = RAW_DATA_DIR / "historical_data.csv"
FEAR_GREED_DATA_PATH: Path = RAW_DATA_DIR / "fear_greed_index.csv"
MERGED_DATASET_PATH: Path = PROCESSED_DATA_DIR / "merged_dataset.csv"
