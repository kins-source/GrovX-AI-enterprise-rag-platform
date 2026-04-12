import time
from functools import wraps
from utils.logger import logger

def track_latency(func):
    """Decorator to track function latency."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        latency = time.time() - start_time
        logger.info(f"Execution time for {func.__name__}: {latency:.4f} seconds")
        return result
    return wrapper

def track_latency_async(func):
    """Decorator to track async function latency."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        latency = time.time() - start_time
        logger.info(f"Execution time for {func.__name__}: {latency:.4f} seconds")
        return result
    return wrapper
