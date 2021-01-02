import time
from unittest import TestCase

import fakeredis
from api_throttler import FixedWindowThrottlerRedis


class TestFixedWindowThrottlerRedis(TestCase):

    def setUp(self) -> None:
        self.cache = fakeredis.FakeStrictRedis()
        self.throttler = FixedWindowThrottlerRedis(calls=2, period=5, cache=self.cache)

    def tearDown(self) -> None:
        self.cache.flushall()

    def test_continuous_calls(self):
        allowed_calls = 0
        for i in range(5):
            if not self.throttler.is_throttled(key="test_key"):
                allowed_calls += 1
            time.sleep(1)
        self.assertEqual(allowed_calls, 2)

    def test_periodic_calls(self):
        allowed_calls = 0
        for i in range(10):
            if i in {0, 4, 5, 6}:
                if not self.throttler.is_throttled(key="test_key"):
                    allowed_calls += 1
            time.sleep(1)
        self.assertEqual(allowed_calls, 4)
