from datetime import datetime, timedelta
from collections import deque

from api_throttler.throttler import Throttler


class SlidingWindowThrottler(Throttler):
    """
    Sliding Window API rate throttler
    """
    def __init__(self, calls: int = 15, period: int = 900):
        super().__init__(calls, period)

    def is_throttled(self, key: str) -> bool:
        """ Return if the API call with a given key is throttled """
        cur_ts = datetime.utcnow()
        if key not in self.hash_table:
            self.hash_table[key] = deque([])
        while self.hash_table[key] and (cur_ts - self.hash_table[key][0] > timedelta(seconds=self.period)):
            self.hash_table[key].popleft()

        if len(self.hash_table[key]) + 1 > self.calls:
            return True
        else:
            self.hash_table[key].append(cur_ts)
            return False
