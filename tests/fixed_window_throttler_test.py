from unittest import TestCase
from unittest.mock import patch, MagicMock

from api_throttler import FixedWindowThrottler


class TestFixedWindowThrottler(TestCase):

    def test_dummy(self):
        self.assertEqual(True, True)
