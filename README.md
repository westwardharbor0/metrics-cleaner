# Metrics Cleaner Readme


## Why this exists

If you use a lot of labels with large number of possible values you can grow your `/metrics` endpoint huge.
This endpoint will never be cleared if you don't restart your service and can grow until your scrapers start to timeout when reading those metrics.
This utils helps you clear those metrics from time to time and keep your scraping times low.

## Install
`poetry add metrics-cleaner` or `pip install metrics-cleaner` 

## How to use it

This tool can be used using a `class` or simply calling onetime methods.

### Class
```python
from metrics_cleaner import MetricsCleaner
# ... Setup your metrics and collector_registry ...
cleaner = MetricsCleaner(collector_registry)
# Clean desired metrics.
cleaner.clean("metrics_name") # Empty one metric by name.
cleaner.clean_all() # Empty all metrics.
```

### Methods
```python
from metrics_cleaner import clean_all_metrics, clean_metrics
# ... Setup your metrics and collector_registry ...
clean_all_metrics(collector_registry) # Empty all metrics.
clean_metrics(collector_registry, "metrics_name") # Empty one metric by name.
```