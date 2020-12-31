from abc import ABCMeta, abstractmethod


class Throttler(metaclass=ABCMeta):
    """ API rate throttler base class """
    def __init__(self, calls: int = 15, period: int = 900):
        """
        :param calls: Number of API calls allowed within a specified time period.
        :param period: The specified time period in seconds
        """
        self.calls = calls
        self.period = period
        self.hash_table = dict()

    @abstractmethod
    def is_throttled(self, key: str) -> bool:
        pass
