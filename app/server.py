#!/usr/bin/env python3
import  os, redis, time, platform
from flask import Flask, make_response, render_template
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

REDIS_HOST=os.getenv('REDIS_HOST', 'redis')

cache = redis.Redis(host=REDIS_HOST, port=6379)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                #raise exc
                return "'No Redis Connection'"
            retries -= 1
            #time.sleep(0.1)

@app.route('/')
@nocache
def hello():
    count = get_hit_count()
    host=platform.node()
    DOCKER_SERVICE_NAME=os.getenv('DOCKER_SERVICE_NAME', host)
    if "{{" in DOCKER_SERVICE_NAME or "}}" in DOCKER_SERVICE_NAME:
        DOCKER_SERVICE_NAME="N/A"
    FOO=os.getenv('FOO', 'unset')
    REDIS_HOST=os.getenv("REDIS_HOST",'unset')
    print(f"Getting visits! {count}")
    return render_template('index.html',visit_counts=count, hostname=host, DOCKER_SERVICE_NAME=DOCKER_SERVICE_NAME, FOO=FOO , redis_host=REDIS_HOST)

@app.route('/health')
def health():
    return "Im healthy"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

