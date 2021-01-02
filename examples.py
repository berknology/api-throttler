import time

import fakeredis
from api_throttler import Throttler, FixedWindowThrottler, SlidingWindowThrottler
from api_throttler import FixedWindowThrottlerRedis, SlidingWindowThrottlerRedis

# Limit 3 calls per 10 seconds
fixed_window_throttler = FixedWindowThrottler(calls=3, period=10)
sliding_window_throttler = SlidingWindowThrottler(calls=3, period=10)

cache = fakeredis.FakeStrictRedis()
fixed_window_throttler_redis = FixedWindowThrottlerRedis(calls=3, period=10, cache=cache)
sliding_window_throttler_redis = SlidingWindowThrottlerRedis(calls=3, period=10, cache=cache)


def call_api(throttler: Throttler, key: str = 'some_string_key'):
    if not throttler.is_throttled(key):
        print('API call is NOT throttled')
    else:
        print('API call is throttled')


print('Using fixed window API throttler')
for i in range(20):
    print(f'This is the {i}-th second')
    # Call API in the following i-th seconds
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(fixed_window_throttler)
    time.sleep(1)

print('-' * 40)

print('Using sliding window API throttler')
for i in range(20):
    print(f'This is the {i}-th second')
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(sliding_window_throttler)
    time.sleep(1)

print('-' * 40)

print('Using fixed window API throttler Redis')
for i in range(20):
    print(f'This is the {i}-th second')
    # Call API in the following i-th seconds
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(fixed_window_throttler_redis)
    time.sleep(1)

print('-' * 40)

print('Using sliding window API throttler Redis')
for i in range(20):
    print(f'This is the {i}-th second')
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(sliding_window_throttler_redis)
    time.sleep(1)
