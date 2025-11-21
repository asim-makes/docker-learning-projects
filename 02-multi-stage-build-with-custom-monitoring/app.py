from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'app_http_requests_total',
    'Total number of HTTP requests to the application',
    ['method', 'endpoint']
)


@app.route("/")
def home():
    time.sleep(0.05)

    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()

    return "Hello from the Optimized Microservice!", 200

@app.route("/metrics")
def metrics():
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics').inc()

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
