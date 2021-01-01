import redis
from flask import Flask, request
from api_throttler import SlidingWindowThrottler, SlidingWindowThrottlerRedis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# throttler = SlidingWindowThrottler(calls=3, period=10)
throttler = SlidingWindowThrottlerRedis(calls=3, period=10, cache=cache)


@app.route('/')
def is_throttled():
    if 'user' in request.args:
        user = request.args['user']
    else:
        user = 'nobody'
    if not throttler.is_throttled(user):
        return f'You are Not throttled, {user}.'
    else:
        return f'You are throttled, {user}.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
