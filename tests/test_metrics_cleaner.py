from unittest import TestCase

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, Summary

from metrics_cleaner import MetricsCleaner


class TestMetricsCleaner(TestCase):
    def setUp(self) -> None:
        collector_registry = CollectorRegistry()
        # Create some example metrics.
        errors = Counter(
            "example_errors_total",
            "",
            labelnames=["example_label"],
            registry=collector_registry,
        )
        runs = Counter(
            "example_runs_total",
            "",
            labelnames=[],
            registry=collector_registry,
        )
        steps = Gauge(
            "example_steps_total",
            "",
            labelnames=[],
            registry=collector_registry,
        )
        hists = Histogram(
            "example_hists",
            "",
            labelnames=["example_label"],
            registry=collector_registry,
        )
        hists_2 = Histogram(
            "example_hists_2",
            "",
            labelnames=[],
            registry=collector_registry,
        )
        sumsum = Summary(
            "example_sum",
            "",
            labelnames=[],
            registry=collector_registry,
        )
        # Add some values to metrics.
        errors.labels("test_label_val_2").inc(42)
        errors.labels("test_label_val_1").inc(42)
        runs.inc(42)
        steps.dec(1)
        hists.labels("test_label_val_2").observe(12)
        hists_2.observe(22)
        sumsum.observe(24)
        sumsum.observe(42)
        # Check we have initial state correct.
        self.assertEqual(
            collector_registry._names_to_collectors["example_runs_total"]._value._value,
            42,
        )
        # Set the instances to class.
        self.metrics_cleaner = MetricsCleaner(collector_registry)
        self.collector_registry = collector_registry

    def testCleanAll(self):
        """Test we can drop all values."""
        self.metrics_cleaner.clean_all()
        self.assertEqual(
            self.collector_registry._names_to_collectors[
                "example_runs_total"
            ]._value._value,
            0,
        )
        self.assertEqual(
            self.collector_registry._names_to_collectors[
                "example_errors_total"
            ]._metrics,
            {},
        )
        self.assertEqual(
            self.collector_registry._names_to_collectors["example_sum"]._count._value,
            0,
        )
        self.assertEqual(
            self.collector_registry._names_to_collectors["example_hists_2"]
            ._buckets[0]
            ._value,
            0,
        )

    def testCleanLabels(self):
        """Test we can drop only requested metric without labels."""
        self.metrics_cleaner.clean("example_runs_total")
        self.assertEqual(
            self.collector_registry._names_to_collectors[
                "example_runs_total"
            ]._value._value,
            0,
        )
        self.assertNotEqual(
            self.collector_registry._names_to_collectors[
                "example_errors_total"
            ]._metrics,
            {},
        )
        self.assertNotEqual(
            self.collector_registry._names_to_collectors["example_hists"]._metrics,
            {},
        )

    def testCleanBasic(self):
        """Test we can drop only requested metric with labels."""
        self.metrics_cleaner.clean("example_errors_total")
        self.assertEqual(
            self.collector_registry._names_to_collectors[
                "example_runs_total"
            ]._value._value,
            42,
        )
        self.assertEqual(
            self.collector_registry._names_to_collectors[
                "example_errors_total"
            ]._metrics,
            {},
        )

    def testMetricsNames(self):
        """Test we are returning metrics names."""
        self.assertTrue("example_errors_total" in self.metrics_cleaner.metric_names())
        self.assertTrue("example_runs_total" in self.metrics_cleaner.metric_names())
        self.assertTrue("example_steps_total" in self.metrics_cleaner.metric_names())
        self.assertTrue("example_sum" in self.metrics_cleaner.metric_names())
        self.assertTrue("example_hists" in self.metrics_cleaner.metric_names())
        self.assertTrue("example_hists_2" in self.metrics_cleaner.metric_names())
