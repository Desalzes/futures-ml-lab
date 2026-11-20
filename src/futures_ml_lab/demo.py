"""Toy smoke demo. THESE NUMBERS ARE NOT REAL MARKET RESULTS."""
from .baseline import SoftmaxBaseline, multiclass_log_loss
from .contracts import ExecutionCosts
from .features import causal_features
from .labels import label_candidate
from .synthetic import make_candidates, make_synthetic_bars


def main() -> None:
    bars = make_synthetic_bars()
    candidates = make_candidates(bars)
    index = {bar.closed_at: i for i, bar in enumerate(bars)}
    examples = [(causal_features(bars, index[c.signal_at]), label_candidate(bars, c, ExecutionCosts(0.25, 0.2)))
                for c in candidates]
    split = int(0.65 * len(examples))
    train, test = examples[:split], examples[split:]
    model = SoftmaxBaseline()
    model.fit([x for x, _ in train], [y.event for _, y in train])
    pred = model.predict_proba([x for x, _ in test])
    loss = multiclass_log_loss(pred, [y.event for _, y in test])
    print("SYNTHETIC SMOKE TEST ONLY. No real market data or validated trading results.")
    print(f"Synthetic candidates: {len(candidates)}; train: {len(train)}; test: {len(test)}")
    print(f"Synthetic test log-loss: {loss:.4f} (checks mechanics only)")


if __name__ == "__main__":
    main()
