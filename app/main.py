from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI(title="DevOps Mini App")

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["path", "method", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    path = request.url.path
    REQUEST_LATENCY.labels(path=path).observe(duration)
    REQUEST_COUNT.labels(path=path, method=request.method, status=str(response.status_code)).inc()
    return response

@app.get("/")
def root():
    return {"message": "Hello from DevOps Mini App 🚀"}

@app.get("/health", response_class=PlainTextResponse)
def health():
    return "OK"

@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
