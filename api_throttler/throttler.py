from typing import Optional
from abc import ABCMeta, abstractmethod

from redis import Redis


class Throttler(metaclass=ABCMeta):
    """ API rate throttler base class """
    def __init__(self, calls: int, period: int, cache: Optional[Redis] = None):
        """
        :param calls: Number of API calls allowed within a specified time period.
        :param period: The specified time period in seconds
        :param cache: a cache to quickly save and retrieve information
        """
        self.calls = calls
        self.period = period
        self.cache = cache if cache else dict()

    @abstractmethod
    def is_throttled(self, key: str) -> bool:
        pass
