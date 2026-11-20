"""Deliberately artificial OHLCV data for unit and API tests ONLY."""
from datetime import datetime, timedelta, timezone
from random import Random

from .contracts import Bar, Candidate


def make_synthetic_bars(n: int = 1600, seed: int = 7) -> list[Bar]:
    if n < 5:
        raise ValueError("n must be at least 5")
    rng = Random(seed)
    start = datetime(2026, 1, 5, 14, 30, tzinfo=timezone.utc)
    price = 20000.0
    result = []
    for i in range(n):
        close = max(1.0, price + rng.gauss(0, 3.0))
        upper = abs(rng.gauss(0, 1.5))
        lower = abs(rng.gauss(0, 1.5))
        high, low = max(price, close) + upper, min(price, close) - lower
        result.append(Bar(start + timedelta(minutes=i), price, high, low, close,
                          max(0.0, 1000.0 + rng.gauss(0, 200.0)), "NQ", "SYNTHETIC"))
        price = close
    return result


def make_candidates(bars: list[Bar], *, every: int = 25, horizon: int = 12) -> list[Candidate]:
    out = []
    for i in range(40, len(bars) - horizon - 1, every):
        side = "long" if bars[i].close >= bars[i - 1].close else "short"
        out.append(Candidate(bars[i].closed_at, side, 6.0, 12.0, horizon, f"synthetic-{i}"))
    return out
