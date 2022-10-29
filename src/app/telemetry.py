from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

import psycopg2
from opentelemetry.instrumentation.dbapi import trace_integration


def init_tracer(args):
    """
    Tracing configuration using OpenTelemetry
    """
    resource = Resource.create(attributes={"service.namespace": "io.testruction",
                                           "service.name": "pytest-sqlalchemy"})


    provider = TracerProvider()
    # processor = BatchSpanProcessor(ConsoleSpanExporter())
    # provider.add_span_processor(processor)
    
    
    otlp_exporter = OTLPSpanExporter()
    otlp_processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(otlp_processor)
    
    trace.set_tracer_provider(provider)

    if args.trace_stdout:
        trace.get_tracer_provider().add_span_processor(
            SimpleSpanProcessor(ConsoleSpanExporter()))
    
    trace_integration(connect_module=psycopg2,
                      connect_method_name="connect",
                      database_system="postgresql")