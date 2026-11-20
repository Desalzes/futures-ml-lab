"""Illustrative next-open triple-barrier label with conservative intrabar policy.

This is NOT an exchange-validated fill engine and must not be represented as one.
"""
from __future__ import annotations

from datetime import timedelta
from typing import Sequence

from .contracts import Bar, Candidate, ExecutionCosts, Outcome


def label_candidate(bars: Sequence[Bar], candidate: Candidate, costs: ExecutionCosts) -> Outcome:
    positions = [i for i, b in enumerate(bars) if b.closed_at == candidate.signal_at]
    if len(positions) != 1:
        raise ValueError("Candidate signal_at must match one bar close")
    signal_index = positions[0]
    entry_index = signal_index + 1
    end_index = entry_index + candidate.horizon_bars - 1
    if end_index >= len(bars):
        raise ValueError("Insufficient subsequent bars for full label horizon")
    block = bars[signal_index:end_index + 1]
    for a, b in zip(block, block[1:]):
        if (b.closed_at - a.closed_at) != timedelta(minutes=1):
            raise ValueError("Cannot label through missing bars / breaks")
        if (a.symbol, a.contract) != (b.symbol, b.contract):
            raise ValueError("Cannot label across symbol or contract roll")

    sign = 1 if candidate.side == "long" else -1
    slip = costs.slippage_points_per_fill
    entry = bars[entry_index].open + sign * slip
    stop = entry - sign * candidate.stop_points
    target = entry + sign * candidate.target_points
    for idx in range(entry_index, end_index + 1):
        bar = bars[idx]
        # At a next-bar open through the stop, a stop-market fills at the worse open.
        # At a next-bar open through the target, take target (no favorable gap bonus).
        stop_gap = (bar.open <= stop) if sign == 1 else (bar.open >= stop)
        target_gap = (bar.open >= target) if sign == 1 else (bar.open <= target)
        stop_touched = (bar.low <= stop) if sign == 1 else (bar.high >= stop)
        target_touched = (bar.high >= target) if sign == 1 else (bar.low <= target)
        if stop_touched:
            raw_exit = (min(stop, bar.open) if sign == 1 else max(stop, bar.open)) if stop_gap else stop
            exit_price = raw_exit - sign * slip
            return Outcome(candidate.candidate_id, "stop", (bars[entry_index].closed_at - timedelta(minutes=1)),
                           bar.closed_at, entry, exit_price,
                           (sign * (exit_price - entry) - costs.round_trip_fee_points) / candidate.stop_points,
                           ambiguous_stop_first=(stop_touched and target_touched and not (stop_gap or target_gap)))
        if target_touched:
            # A limit take-profit is not guaranteed by OHLC; this simplified path is
            # optimistic about being filled if the price touches. Stress separately.
            raw_exit = target
            exit_price = raw_exit - sign * slip
            return Outcome(candidate.candidate_id, "target", (bars[entry_index].closed_at - timedelta(minutes=1)),
                           bar.closed_at, entry, exit_price,
                           (sign * (exit_price - entry) - costs.round_trip_fee_points) / candidate.stop_points)
    exit_bar = bars[end_index]
    exit_price = exit_bar.close - sign * slip
    return Outcome(candidate.candidate_id, "timeout", (bars[entry_index].closed_at - timedelta(minutes=1)),
                   exit_bar.closed_at, entry, exit_price,
                   (sign * (exit_price - entry) - costs.round_trip_fee_points) / candidate.stop_points)
