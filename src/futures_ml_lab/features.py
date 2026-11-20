"""A deliberately simple *causal* benchmark feature set."""
from __future__ import annotations

from datetime import timedelta
from math import sqrt
from typing import Sequence

from .contracts import Bar, FeatureRow


def causal_features(bars: Sequence[Bar], index: int, lookback: int = 20) -> FeatureRow:
    """Return a feature vector observable at close of bars[index] only.

    No global mean/variance is fit across evaluation samples. Local normalization
    uses the window ending at index. Bars must be contiguous in contract and time.
    """
    if lookback < 3 or index < lookback or index >= len(bars):
        raise ValueError("Need at least lookback closed prior bars")
    window = bars[index - lookback:index + 1]
    for left, right in zip(window, window[1:]):
        if (right.closed_at - left.closed_at) != timedelta(minutes=1):
            raise ValueError("Missing or irregular 1-minute bar in feature window")
        if (right.symbol, right.contract) != (left.symbol, left.contract):
            raise ValueError("Feature window crosses instrument/contract boundary")
    current = window[-1]
    previous = window[-2]
    returns = [(b.close / a.close - 1.0) for a, b in zip(window, window[1:])]
    mean_ret = sum(returns) / len(returns)
    realized_vol = sqrt(sum((r - mean_ret) ** 2 for r in returns) / len(returns))
    mean_volume = sum(b.volume for b in window[:-1]) / lookback
    relative_volume = current.volume / mean_volume if mean_volume else 0.0
    candle_range = current.high - current.low
    candle_location = (current.close - current.low) / candle_range if candle_range else 0.5
    names = ("last_return", "lookback_return", "realized_vol", "range_fraction", "volume_ratio", "candle_location")
    values = (returns[-1], current.close / window[0].close - 1.0, realized_vol,
              candle_range / current.close, relative_volume, candle_location)
    return FeatureRow(as_of=current.closed_at, names=names, values=values)
