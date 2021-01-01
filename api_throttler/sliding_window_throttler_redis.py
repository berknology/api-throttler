from typing import Union
from datetime import datetime, timedelta

from redis import Redis
from api_throttler.throttler import Throttler


class SlidingWindowThrottlerRedis(Throttler):
    """
    Sliding Window API rate throttler using Redis
    """
    def __init__(self, cache: Redis, calls: int = 15, period: int = 900):
        super().__init__(calls, period, cache)

    def is_throttled(self, key: str) -> bool:
        """ Return if the API call with a given key is throttled """
        cur_ts = datetime.utcnow()

        while (self.cache.llen(key) > 0) and self._is_head_obsolete(cur_ts, self.cache.lrange(key, 0, 0)[0]):
            self.cache.lpop(key)

        if self.cache.llen(key) + 1 > self.calls:
            return True
        else:
            self.cache.rpush(key, str(cur_ts))
            return False

    def _is_head_obsolete(self, cur_ts: datetime, queue_head: Union[bytes, str]) -> bool:
        if isinstance(queue_head, bytes):
            queue_head = queue_head.decode("utf-8")
        ts = datetime.strptime(queue_head, '%Y-%m-%d %H:%M:%S.%f')
        return cur_ts - ts > timedelta(seconds=self.period)
