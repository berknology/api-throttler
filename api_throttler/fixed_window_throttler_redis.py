from redis import Redis
from api_throttler.throttler import Throttler


class FixedWindowThrottlerRedis(Throttler):
    """
    Fixed Window API rate throttler using Redis
    """
    def __init__(self, cache: Redis, calls: int = 15, period: int = 900):
        super().__init__(calls, period, cache)

    def is_throttled(self, key: str) -> bool:
        """ Return if the API call with a given key is throttled """
        if self.cache.setnx(key, 0):
            self.cache.expire(key, self.period)
        self.cache.incr(key)
        return int(self.cache.get(key)) > self.calls
