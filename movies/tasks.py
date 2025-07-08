import logging
from shared.config.settings import redis_broker

logger = logging.getLogger(__name__)


@redis_broker.task()
def process_heavy_task(max_count=1_000_000_000):
    count = 0

    while count < max_count:
        count += 1
        if count % max_count == 0:
            logger.info("==============================================")
            logger.info("Successfully Processed 1 Billion Transactions...")
            logger.info("==============================================")

    return count
