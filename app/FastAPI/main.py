import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor

# ✅ Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

# ✅ Set up tracer provider with resource name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "fastapi-backend"})
    )
)

# ✅ Configure OTLP trace exporter (to OTEL Collector)
collector_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "collector:4317")


otlp_exporter = OTLPSpanExporter(
    endpoint=collector_endpoint,
    insecure=True
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# ✅ Initialize FastAPI
app = FastAPI(title="FastAPI Backend")

# ✅ Instrument FastAPI and HTTP clients
FastAPIInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
URLLibInstrumentor().instrument()

# ✅ Expose Prometheus metrics
Instrumentator().instrument(app).expose(app)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routes
@app.get("/")
def read_root():
    logger.info("✅ GET / called")
    return {"message": "Hello from FastAPI backend!"}

@app.get("/api/health")
def health_check():
    logger.info("✅ GET /api/health called")
    return {"status": "ok"}

@app.get("/api/message")
def get_message():
    logger.info("✅ GET /api/message called")
    return {"message": "Hello from FastAPI API"}

@app.get("/trace")
def trace_test():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("custom-span-trace"):
        logger.info("✅ Custom span 'custom-span-trace' created and sent to OTEL Collector")
        return {"message": "This route creates a custom trace span!"}
