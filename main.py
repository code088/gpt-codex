import asyncio
import logging
from src.config import LOG_LEVEL, LOG_FORMAT, LOG_FILE_PATH
from src.tasks import sample_task

def configure_logging() -> None:
    """Configure application-wide logging."""
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE_PATH)
        ]
    )

async def run() -> None:
    """Run sample asynchronous tasks."""
    await sample_task()
    try:
        await sample_task(should_fail=True)
    except Exception:
        logging.getLogger(__name__).info("Handled exception from failing task")

if __name__ == "__main__":
    configure_logging()
    asyncio.run(run())
