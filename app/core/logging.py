import logging
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Log file path
LOG_FILE = BASE_DIR / "app.log"


def setup_logging():

    logging.basicConfig(
        level=logging.INFO,

        format=(
            "%(asctime)s - "
            "%(name)s - "
            "%(levelname)s - "
            "%(message)s"
        ),

        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ],

        force=True
    )
