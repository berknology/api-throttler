==================================================
API Throttler
==================================================

A Python toolkit to enforce API rate limit on the backend.

Usage
-----
To use this API throttler toolkit, first install it using pip:

.. code-block:: bash

    pip install api-throttler


Then, import the package in your python script and use appropriate throttler classes:

.. code-block:: python

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
