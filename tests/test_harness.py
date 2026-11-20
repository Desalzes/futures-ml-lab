import unittest
from dataclasses import replace
from datetime import timedelta

from futures_ml_lab.baseline import SoftmaxBaseline
from futures_ml_lab.contracts import Bar, Candidate, ExecutionCosts
from futures_ml_lab.features import causal_features
from futures_ml_lab.labels import label_candidate
from futures_ml_lab.synthetic import make_candidates, make_synthetic_bars


class HarnessTests(unittest.TestCase):
    def test_prefix_invariance(self):
        bars = make_synthetic_bars(100)
        original = causal_features(bars, 50)
        modified = bars[:51] + [replace(b, close=b.close + 10000, high=b.high + 10000)
                                for b in bars[51:]]
        self.assertEqual(original, causal_features(modified, 50))

    def test_next_open_not_signal_close(self):
        bars = make_synthetic_bars(8)
        signal = bars[1]
        bars[2] = replace(bars[2], open=bars[2].open + 1,
                          high=max(bars[2].high, bars[2].open + 1))
        candidate = Candidate(signal.closed_at, "long", 1000, 2000, 2, "next-open")
        outcome = label_candidate(bars, candidate, ExecutionCosts())
        self.assertEqual(outcome.entry_price, bars[2].open)
        self.assertEqual(outcome.entered_at, signal.closed_at)

    def test_stop_first_on_double_touch(self):
        bars = make_synthetic_bars(10)
        signal = bars[2]
        entry_bar = bars[3]
        e = entry_bar.open
        bars[3] = replace(entry_bar, high=e + 10, low=e - 10, close=e)
        candidate = Candidate(signal.closed_at, "long", 5, 5, 2, "double-touch")
        out = label_candidate(bars, candidate, ExecutionCosts())
        self.assertEqual(out.event, "stop")
        self.assertTrue(out.ambiguous_stop_first)
        self.assertAlmostEqual(out.net_r, -1.0)

    def test_short_stop_first(self):
        bars = make_synthetic_bars(10)
        e = bars[3].open
        bars[3] = replace(bars[3], high=e + 10, low=e - 10, close=e)
        out = label_candidate(bars, Candidate(bars[2].closed_at, "short", 5, 5, 2, "short"), ExecutionCosts())
        self.assertEqual(out.event, "stop")
        self.assertTrue(out.ambiguous_stop_first)

    def test_contract_roll_or_gap_rejected(self):
        bars = make_synthetic_bars(10)
        bars[4] = replace(bars[4], contract="NEXT")
        with self.assertRaises(ValueError):
            label_candidate(bars, Candidate(bars[2].closed_at, "long", 1, 1, 3, "roll"), ExecutionCosts())
        bars = make_synthetic_bars(25)
        bars[10] = replace(bars[10], closed_at=bars[10].closed_at + timedelta(seconds=1))
        with self.assertRaises(ValueError):
            causal_features(bars, 12, lookback=5)

    def test_costs_reduce_net_r(self):
        bars = make_synthetic_bars(8)
        candidate = Candidate(bars[2].closed_at, "long", 1000, 2000, 2, "cost")
        gross = label_candidate(bars, candidate, ExecutionCosts())
        net = label_candidate(bars, candidate, ExecutionCosts(round_trip_fee_points=2.0))
        self.assertAlmostEqual(gross.net_r - net.net_r, 0.002)

    def test_feature_schema_and_baseline(self):
        bars = make_synthetic_bars(900)
        index = {b.closed_at: i for i, b in enumerate(bars)}
        candidates = make_candidates(bars)
        rows = [causal_features(bars, index[c.signal_at]) for c in candidates]
        labels = [label_candidate(bars, c, ExecutionCosts()).event for c in candidates]
        train_end = int(0.7 * len(rows))
        model = SoftmaxBaseline(steps=30)
        model.fit(rows[:train_end], labels[:train_end])
        result = model.predict_proba(rows[train_end:])
        self.assertTrue(result)
        for probs in result:
            self.assertAlmostEqual(sum(probs.values()), 1.0, places=10)
            self.assertEqual(set(probs), {"stop", "target", "timeout"})
        self.assertEqual(model.names, rows[0].names)

    def test_bad_ohlc_rejected(self):
        b = make_synthetic_bars(5)[0]
        with self.assertRaises(ValueError):
            replace(b, high=b.open - 1)


if __name__ == "__main__":
    unittest.main()
