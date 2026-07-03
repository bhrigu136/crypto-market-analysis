"""Central filesystem paths used throughout the project."""

from pathlib import Path


PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
PLOTS_DIR: Path = PROJECT_ROOT / "plots"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"

HISTORICAL_DATA_PATH: Path = RAW_DATA_DIR / "historical_data.csv"
FEAR_GREED_DATA_PATH: Path = RAW_DATA_DIR / "fear_greed_index.csv"
