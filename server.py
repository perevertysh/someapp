import os

from bottle import Bottle, request, response, route, run

from dotenv import load_dotenv

import sentry_sdk
from sentry_sdk.integrations.bottle import BottleIntegration

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[BottleIntegration()]
)


@route('/')
def index():
    # raise RuntimeError("There is an error!")
    response.body = "index"
    return response


@route('/success')
def success():
    response.body = "success"
    response.status = 200
    return response


@route('/fail')
def fail():
    response.body = "fail"
    response.status = 500
    raise Exception(str(dict(os.environ)))
    return response


if os.environ.get("APP_LOCATION") == "heroku":
    run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    run(host="0.0.0.0", port=8080, debug=True)
