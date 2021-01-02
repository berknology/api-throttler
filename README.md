API Throttler
=============

![Build](https://github.com/berknology/api-throttler/workflows/Build/badge.svg)
![Release](https://github.com/berknology/api-throttler/workflows/Release/badge.svg)
![PyPi](https://img.shields.io/pypi/v/api-throttler.svg)


A Python toolkit to enforce API rate limit on the backend. The toolkit enable the service backend to limit the number of 
API calls in a specified period, e.g., 15 API calls per 900 seconds. There are four throttler classes in the toolkit:
  * FixedWindowThrottler
  * SlidingWindowThrottler
  * FixedWindowThrottlerRedis
  * SlidingWindowThrottlerRedis

The first two throttler classes use local storage to save throttler data (e.g., API calls that have been served and 
their timestamps), while the last two throttler classes use a Redis server to store throttler information. The 
difference between the fixed window and sliding window throttlers is the fixed window throttler uses the timestamp when 
the first feasible request is served as the starting timestamp to determine the number of allowed API calls in the 
following period, while the sliding window throttler uses the current timestamp minus the specified period as the 
starting timestamp to calculate the number of allowed API calls. The advantage of fixed window throttler is its 
simplicity, but there could be many API calls allowed if they are at the end of last period and the beginning of the 
current period. On the other hand, the sliding window throttler could resolve this issue, but it takes more memory. 


Usage
--------
To use this API throttler toolkit, first install it using pip:
```bash
pip install api-throttler
```

Then, import the package in your python script and use appropriate throttler classes:

```python
import time

from api_throttler import Throttler, FixedWindowThrottler, SlidingWindowThrottler


# Limit 3 calls per 10 seconds
fixed_window_throttler = FixedWindowThrottler(calls=3, period=10)
sliding_window_throttler = SlidingWindowThrottler(calls=3, period=10)


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
    
print('-'*40)

print('Using sliding window API throttler')
for i in range(20):
    print(f'This is the {i}-th second')
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(sliding_window_throttler)
    time.sleep(1)
```

In the above example, the data of the throttler is saved in local memory. If you would like to save it in a redis 
server, you can use the `FixedWindowThrottlerRedis` and `SlidingWindowThrottlerRedis` classes. The following scripts 
shows how to use the two classes using [fake redis](https://github.com/jamesls/fakeredis):

```python
import time

import fakeredis
from api_throttler import Throttler, FixedWindowThrottlerRedis, SlidingWindowThrottlerRedis

cache = fakeredis.FakeStrictRedis()

# Limit 3 calls per 10 seconds
fixed_window_throttler = FixedWindowThrottlerRedis(calls=3, period=10, cache=cache)
sliding_window_throttler = SlidingWindowThrottlerRedis(calls=3, period=10, cache=cache)


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
    
print('-'*40)

print('Using sliding window API throttler')
for i in range(20):
    print(f'This is the {i}-th second')
    if i in {0, 8, 9, 10, 11, 12}:
        call_api(sliding_window_throttler)
    time.sleep(1)
```

If you would like to try a real example using API served by a Flask app and a redis server, please try to run the 
`app.py` using Docker by typing the following command in your terminal:
```bash
docker-compose up --build
``` 
