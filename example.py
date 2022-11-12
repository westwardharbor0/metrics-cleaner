"""Example code."""
from time import sleep
from metrics_cleaner import MetricsCleaner
from prometheus_client import Histogram, start_http_server, CollectorRegistry, Counter
# Creat the metrics registry.
collector_registry = CollectorRegistry()
# Create some example metrics.
errors = Counter(
    "example_errors_total",
    "Amount of errors.",
    labelnames=["label1", "label2"],
    registry=collector_registry,
)
runs = Counter(
    "example_runs_total",
    "Amount of runs.",
    registry=collector_registry,
)
progress = Histogram(
    "example_progress",
    "Amount of runs.",
    registry=collector_registry,
)
# Create the cleaner instance.
new_cleaner = MetricsCleaner(collector_registry)
start_http_server(9666, registry=collector_registry)
# Add some metric values and clear them.
for step in range(10000):
    if step % 2 == 0:
        progress.observe(step)
        # Add some metric with labels.
        errors.labels("example_service", f"step_{step}").inc(step**2)
    if step % 10 == 0:
        # Drop all the metric values.
        new_cleaner.clean_all()
    # Add some metric with no labels.
    runs.inc()
    sleep(1)
