import logging
from pathlib import Path

# Logging configuration constants
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE_PATH = Path("logs/app.log")
