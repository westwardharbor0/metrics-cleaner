"""MetricsCleaner code storage."""
from prometheus_client import CollectorRegistry


class MetricsCleaner:
    """Simple class to allow user to clean metrics values."""

    def __init__(self, collector_registry: CollectorRegistry):
        self.collector_registry: CollectorRegistry = collector_registry

    def clean(self, metric_name: str):
        """Empty value of given metric by name.

        :param metric_name: Metric name.
        """
        if metric_name not in self.collector_registry._names_to_collectors:
            raise IndexError("Metric name not found in collector registry")
        # Empty all the metrics with labels.
        if hasattr(self.collector_registry._names_to_collectors[metric_name], "_lock"):
            self.collector_registry._names_to_collectors[metric_name].clear()
            return
        # Now empty all the metrics without labels.
        metric_type = self.collector_registry._names_to_collectors[metric_name]._type
        if metric_type == "counter" or metric_type == "gauge":
            self.collector_registry._names_to_collectors[metric_name]._value._value = 0
        elif metric_type == "summary":
            self.collector_registry._names_to_collectors[metric_name]._sum.value = 0
            self.collector_registry._names_to_collectors[metric_name]._count._value = 0
        elif metric_type == "histogram":
            for bucket in range(
                len(self.collector_registry._names_to_collectors[metric_name]._buckets)
            ):
                self.collector_registry._names_to_collectors[metric_name]._buckets[
                    bucket
                ]._value = 0

    def clean_all(self):
        """Empty value of all metrics assigned to collector."""
        for collector in self.collector_registry._names_to_collectors:
            # Iterate through all metric names and clear them.
            self.clean(collector)

    def metric_names(self) -> list[str]:
        """Get all the metric names in collector.

        :return: List of metric names in collector.
        """
        return list(self.collector_registry._names_to_collectors.keys())


def clean_all_metrics(collector_registry: CollectorRegistry):
    """Simple all metrics values clean without using the whole class."""
    mc = MetricsCleaner(collector_registry)
    mc.clean_all()


def clean_metrics(collector_registry: CollectorRegistry, metric_name: str):
    """Simple all metric value clean without using the whole class."""
    mc = MetricsCleaner(collector_registry)
    mc.clean(metric_name)
