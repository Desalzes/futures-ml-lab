"""Small public integration contract; no dependency on a private backtester."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Literal, Protocol, Sequence

Side = Literal["long", "short"]
Event = Literal["target", "stop", "timeout"]


@dataclass(frozen=True)
class Bar:
    """One completed 1-minute OHLCV bar. `closed_at` is timezone-aware bar END time.

    A real-data adapter MUST resolve its feed's open/close timestamp convention,
    session calendar, contract and timezone before constructing Bar instances.
    """
    closed_at: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    symbol: str = "NQ"
    contract: str = "SYNTHETIC"

    def __post_init__(self) -> None:
        if self.closed_at.tzinfo is None or self.closed_at.utcoffset() is None:
            raise ValueError("Bar.closed_at must be timezone-aware")
        if not all(isfinite(v) for v in (self.open, self.high, self.low, self.close, self.volume)):
            raise ValueError("Bar contains non-finite OHLCV")
        if self.open <= 0 or self.close <= 0 or self.low <= 0:
            raise ValueError("Expected strictly positive prices")
        if self.low > min(self.open, self.close) or self.high < max(self.open, self.close):
            raise ValueError("Invalid OHLC bar")
        if self.volume < 0 or not self.symbol or not self.contract:
            raise ValueError("Invalid volume/symbol/contract")


@dataclass(frozen=True)
class Candidate:
    """A trade idea formed *after* a signal bar has closed, before its next open."""
    signal_at: datetime
    side: Side
    stop_points: float
    target_points: float
    horizon_bars: int
    candidate_id: str

    def __post_init__(self) -> None:
        if self.side not in ("long", "short"):
            raise ValueError("side must be long or short")
        if not self.candidate_id or self.stop_points <= 0 or self.target_points <= 0 or self.horizon_bars < 1:
            raise ValueError("Invalid candidate fields")
        if not isfinite(self.stop_points) or not isfinite(self.target_points):
            raise ValueError("Non-finite stop or target")
        if self.signal_at.tzinfo is None or self.signal_at.utcoffset() is None:
            raise ValueError("Candidate.signal_at must be timezone aware")


@dataclass(frozen=True)
class ExecutionCosts:
    """Illustrative costs in instrument PRICE POINTS, not USD or ticks.

    slippage_points_per_fill: adverse price shift applied on entry and exit.
    round_trip_fee_points: entire round-trip commission converted to points.
    Users must specify instrument-specific costs in actual experiments.
    """
    slippage_points_per_fill: float = 0.0
    round_trip_fee_points: float = 0.0

    def __post_init__(self) -> None:
        for value in (self.slippage_points_per_fill, self.round_trip_fee_points):
            if not isfinite(value) or value < 0:
                raise ValueError("Execution costs must be finite and >= 0")


@dataclass(frozen=True)
class FeatureRow:
    as_of: datetime
    names: tuple[str, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.names or len(self.names) != len(self.values):
            raise ValueError("Feature names and values mismatch")
        if not all(isfinite(v) for v in self.values):
            raise ValueError("Non-finite features")


@dataclass(frozen=True)
class Outcome:
    candidate_id: str
    event: Event
    entered_at: datetime
    exited_at: datetime
    entry_price: float
    exit_price: float
    net_r: float
    ambiguous_stop_first: bool = False


class ProbabilisticTradeModel(Protocol):
    """Adapters should return calibrated class probabilities where practical."""
    def fit(self, x: Sequence[FeatureRow], y: Sequence[Event]) -> None: ...
    def predict_proba(self, x: Sequence[FeatureRow]) -> list[dict[Event, float]]: ...
