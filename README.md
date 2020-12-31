API Throttler
=============

![Build](https://github.com/berknology/api_throttler/workflows/Build/badge.svg)
![Release](https://github.com/berknology/api_throttler/workflows/Release/badge.svg)
![PyPi](https://img.shields.io/pypi/v/api_throttler.svg)


A Python toolkit to enforce API rate limit on the backend.


Usage
--------
To use this API throttler toolkit, first install it using pip:
```bash
pip install api-throttler
```

Then, import the package in your python script and call appropriate functions:

```python
import time

from api_throttler import FixedWindowThrottler


fixed_window_throttler = FixedWindowThrottler(calls=5, period=10)

for i in range(20):
    if not fixed_window_throttler.is_throttled('some_string_key'):
        print(f'The {i}-th API call is NOT limited')
    else:
        print(f'The {i}-th API call is limited')
    time.sleep(1)
```
