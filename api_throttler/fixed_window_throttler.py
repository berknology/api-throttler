from datetime import datetime, timedelta

from api_throttler.throttler import Throttler


class FixedWindowThrottler(Throttler):
    """
    Fixed Window API rate throttler
    """
    def __init__(self, calls: int = 15, period: int = 900):
        super().__init__(calls, period)

    def is_throttled(self, key: str) -> bool:
        """ Return if the API call with a given key is throttled """
        if self._is_fresh_call(key):
            self.cache[key] = \
                {
                    "num_of_calls": 1,
                    "last_call_ts": datetime.utcnow()
                }
        else:
            self.cache[key]["num_of_calls"] += 1

        return self.cache[key]["num_of_calls"] > self.calls

    def _is_fresh_call(self, key: str) -> bool:
        """ Return True if key not in hash table or the time span is greater than specified period """
        return (key not in self.cache) or \
               (datetime.utcnow() - self.cache[key]["last_call_ts"] > timedelta(seconds=self.period))
