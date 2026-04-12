from hashlib import md5
from typing import Optional
from utils.logger import logger

class QueryCache:
    """
    A simple in-memory cache for user queries.
    Designed to be easily swappable with a Redis implementation for production.
    """
    def __init__(self):
        self._cache = {}

    def _generate_key(self, query: str) -> str:
        return md5(query.lower().strip().encode("utf-8")).hexdigest()

    def get(self, query: str) -> Optional[str]:
        key = self._generate_key(query)
        res = self._cache.get(key)
        if res:
            logger.info(f"Cache HIT for query: '{query}'")
        else:
            logger.info(f"Cache MISS for query: '{query}'")
        return res

    def set(self, query: str, response: str):
        key = self._generate_key(query)
        self._cache[key] = response
        logger.debug(f"Cached response for query: '{query}'")

# Global singleton
query_cache = QueryCache()
