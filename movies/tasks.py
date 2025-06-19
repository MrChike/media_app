from shared.config.settings import redis_broker, logger

@redis_broker.task()
def process_heavy_task(max_count = 1_000_000_000):
    count = 0

    while count < max_count:
        count += 1
        if count % max_count == 0:
            logger.info(f"==============================================")
            logger.info(f"Successfully Processed 1 Billion iterations...")
            logger.info(f"==============================================")

    return count