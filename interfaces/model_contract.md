# Model integration contract (v0.1)

The Python types in `src/futures_ml_lab/contracts.py` are the reference interface. These types deliberately do **not** require a private codebase.

## Inputs

- `Bar`: timezone-aware **close timestamp** (`closed_at`), OHLCV, symbol, outright contract. Feed adapters resolve timestamp conventions and contract rolls **before** instantiating it.
- `Candidate`: candidate ID, already-known signal close, side, stop and target distances in **price points**, and maximum horizon in minutes/bars. This is not an executed trade.
- `ExecutionCosts`: round-trip fee converted to price points and adverse slippage in price points **per fill**. Instrument-specific values must be set by the tester; the default zero is for unit tests, not realistic trading.
- `FeatureRow`: immutable feature schema, vector and `as_of` timestamp. Inputs cannot depend on later bars.
- `Outcome`: first target/stop/timeout event, points-based net result expressed in risk multiples, entry and exit timestamps, and whether stop-first was used for simultaneous barrier touches.

## Model interface

```python
class ProbabilisticTradeModel(Protocol):
    def fit(self, x: Sequence[FeatureRow], y: Sequence[Event]) -> None: ...
    def predict_proba(self, x: Sequence[FeatureRow]) -> list[dict[Event, float]]: ...
```

A model may expose a separate causal encoder for frozen embeddings or feature vectors, but should wrap the downstream classifier into this common interface. Class keys are exactly `target`, `stop`, `timeout`; per-row probabilities must sum to 1.0. Record fitted training statistics and checkpoint hashes. For other tasks (MFE/MAE/survival heads) extend the return schema in a separate experimental API without breaking the v0.1 classification contract.

## Causal timing

Example: a 09:30–09:31 one-minute bar with close timestamp **09:31** may be read at 09:31; a candidate generated then fills no earlier than the 09:31 **open of the following** bar if the engine can execute at that instant. The reference label code uses next-bar opening price and costs. A 5-minute aggregation cannot be read until the whole 5-minute interval has closed.

## IMPORTANT: synthetic labeler limitations

`label_candidate` is a **small illustrative label helper, not an exchange fill simulator**. It chooses stop-first on a single bar touching both barriers, models adverse gaps through stops, and assumes target is filled when touched even though touch does not guarantee a passive limit fill. Real testing needs a validated engine, contract-specific tick/fee models, queue-independent realistic fills, and explicit no-trade/session rules.

The helper rejects missing bars and contract transitions inside the full label horizon. It does not model limit order queue priority, partial fills, macroeconomic events, funding, margin or position overlap. That is deliberate.
