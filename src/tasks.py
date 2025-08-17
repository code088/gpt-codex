import asyncio
import logging

logger = logging.getLogger(__name__)

async def sample_task(should_fail: bool = False) -> None:
    """A sample asynchronous task that logs its progress.

    Args:
        should_fail: If True, the task will raise an exception to demonstrate
            logging of errors.
    """
    logger.info("Task started")
    try:
        await asyncio.sleep(0.1)
        if should_fail:
            raise ValueError("Simulated failure")
        logger.info("Task completed successfully")
    except Exception:
        logger.exception("Task failed")
        raise
