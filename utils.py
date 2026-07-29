"""
Shared helpers used across data.py, features.py, model.py, and scripts/train.py.
"""

import time
import yaml
from pathlib import Path
from contextlib import contextmanager


def load_config(path: str | Path = "config.yaml") -> dict:
    """Load the single YAML file that drives training end-to-end."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config not found at {path}")
    with open(path) as f:
        return yaml.safe_load(f)


@contextmanager
def timer():
    """Context manager that yields a dict which will hold {'seconds': float}
    once the `with` block exits -- used to time training and inference
    consistently across all models in Weeks 6-8.

    Usage:
        timing = {}
        with timer() as t:
            model.fit(X_train, y_train)
        t["seconds"]  # populated after the block exits
    """
    result = {}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["seconds"] = time.perf_counter() - start


def per_prediction_ms(total_seconds: float, n_predictions: int) -> float:
    """Convert a total inference time into milliseconds-per-prediction,
    the unit used throughout the Week 7 benchmark table.
    """
    if n_predictions == 0:
        return 0.0
    return round((total_seconds / n_predictions) * 1000, 4)
