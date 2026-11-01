import logging 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE_PATH = BASE_DIR / "app.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()],
        force = True
    )
