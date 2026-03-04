from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor

resource = Resource.create({"service.name": "my-python-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True,
)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

if __name__ == "__main__":

    with tracer.start_as_current_span("span-1") as parent:
        
        span = trace.get_current_span()
        trace_id = format(span.get_span_context().trace_id, "32x")

        for i in range(3):
            with tracer.start_as_current_span(f"trace-{trace_id}-sub-span-{i}"):
                print(f"Working on sub-span {i}...")
                
    print("Sending spans to Tempo.")