"""A dependency-free, intentionally unremarkable softmax baseline.

It demonstrates the model contract; it is not an advanced trading model.
"""
from __future__ import annotations

from math import exp, log
from typing import Sequence

from .contracts import Event, FeatureRow

CLASSES: tuple[Event, ...] = ("target", "stop", "timeout")


class SoftmaxBaseline:
    def __init__(self, steps: int = 400, learning_rate: float = 0.1, l2: float = 0.01):
        self.steps = steps
        self.learning_rate = learning_rate
        self.l2 = l2
        self.names: tuple[str, ...] | None = None
        self.mean: list[float] = []
        self.std: list[float] = []
        self.weights: list[list[float]] = []

    def _transform(self, rows: Sequence[FeatureRow]) -> list[list[float]]:
        if self.names is None:
            raise ValueError("Fit model before predicting")
        out = []
        for row in rows:
            if row.names != self.names:
                raise ValueError("Feature schema mismatch")
            out.append([1.0] + [(a - mu) / sigma for a, mu, sigma in zip(row.values, self.mean, self.std)])
        return out

    @staticmethod
    def _softmax(scores: list[float]) -> list[float]:
        max_score = max(scores)
        nums = [exp(s - max_score) for s in scores]
        denom = sum(nums)
        return [v / denom for v in nums]

    def fit(self, x: Sequence[FeatureRow], y: Sequence[Event]) -> None:
        if not x or len(x) != len(y):
            raise ValueError("Need nonempty equal-length training inputs/labels")
        self.names = x[0].names
        if any(row.names != self.names for row in x):
            raise ValueError("Training rows have different schemas")
        if any(label not in CLASSES for label in y):
            raise ValueError("Unexpected event class")
        dims = len(self.names)
        self.mean = [sum(row.values[j] for row in x) / len(x) for j in range(dims)]
        self.std = [max((sum((row.values[j] - self.mean[j])**2 for row in x) / len(x))**0.5, 1e-12)
                    for j in range(dims)]
        data = self._transform(x)
        self.weights = [[0.0] * (dims + 1) for _ in CLASSES]
        for _ in range(self.steps):
            gradient = [[0.0] * (dims + 1) for _ in CLASSES]
            for features, label in zip(data, y):
                probabilities = self._softmax([sum(w * v for w, v in zip(class_weights, features))
                                               for class_weights in self.weights])
                for k, cls in enumerate(CLASSES):
                    delta = probabilities[k] - (1.0 if label == cls else 0.0)
                    for j, value in enumerate(features):
                        gradient[k][j] += delta * value
            for k in range(len(CLASSES)):
                for j in range(dims + 1):
                    reg = 0.0 if j == 0 else self.l2 * self.weights[k][j]
                    self.weights[k][j] -= self.learning_rate * (gradient[k][j] / len(x) + reg)

    def predict_proba(self, x: Sequence[FeatureRow]) -> list[dict[Event, float]]:
        data = self._transform(x)
        return [dict(zip(CLASSES, self._softmax([sum(w * v for w, v in zip(class_weights, features))
                                               for class_weights in self.weights]))) for features in data]


def multiclass_log_loss(predictions: Sequence[dict[Event, float]], labels: Sequence[Event]) -> float:
    if not predictions or len(predictions) != len(labels):
        raise ValueError("Need equally sized predictions and labels")
    return -sum(log(max(prediction[label], 1e-15)) for prediction, label in zip(predictions, labels)) / len(labels)
