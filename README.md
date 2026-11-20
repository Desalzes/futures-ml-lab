# Futures ML Lab

A **public, self-contained research workbench** for advanced machine learning on NQ/MNQ-style intraday futures bars. Designed for researchers and LLM coding agents that have **no access to anyone's private backtester or market data**.

**Status:** early research scaffold, with a runnable **synthetic-only** harness. No strategy has been validated, no model weights are bundled, no real-market results are asserted, and no order execution is supported.

## What makes this useful

- Six precise experiment briefs covering multi-head barrier modeling, futures foundation-model embeddings, Kronos, JEPA, Mamba/PatchTST, and probabilistic forecaster fusion.
- A small Python package with explicit dataclasses for completed one-minute bars, candidate trades, execution costs, features, and outcomes.
- Synthetic-data baseline, next-open entry model, conservative stop-first label policy and eight automated tests.
- A standardized interface to let multiple independent researchers or LLMs deliver compatible models without a private integration.
- Copy/paste research prompt, agent contribution guidelines and research-result template.

## Data boundary

**Allowed:** OHLCV bars at one minute or causally aggregated higher timeframes. Optional *other OHLCV instruments* (for example ES), calendars or publicly licensed bar datasets can be researched if clearly disclosed.

**Excluded:** L3 / market-by-order, L2 market depth, order books, DOM, queue-position inference, individual order messages and strategies dependent on these streams. A Mamba network reading **bar sequences** is allowed; one reading order-book event messages is not.

**Never upload** private market data, internal research documents, credentials, downloaded proprietary model checkpoints or backtest artifacts. This repository contains no connection to a private trading system.

## Start in 3 minutes

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\\Scripts\\activate
python -m pip install -e .
python -m unittest discover -s tests -v
python -m futures_ml_lab.demo
```

The final command generates artificial OHLCV bars, derives causal features, labels mock candidates and fits a small softmax baseline. It prints **toy** log-loss solely to exercise the interface. It does not indicate trading profitability.

## Choose a task

| ID | Topic | Starting point | State |
|---|---|---|---|
| ML-001 | Barrier outcomes and calibrated trade selection | [Experiment](experiments/ML-001.md) | Open |
| ML-002 | Futures Foundation Model frozen embeddings | [Experiment](experiments/ML-002.md) | Open |
| ML-003 | Kronos candlestick transfer | [Experiment](experiments/ML-003.md) | Open |
| ML-004 | Bar-only JEPA representation learning | [Experiment](experiments/ML-004.md) | Open |
| ML-005 | Mamba-2 versus PatchTST sequence models | [Experiment](experiments/ML-005.md) | Open |
| ML-006 | Chronos-2, FinCast, and fusion | [Experiment](experiments/ML-006.md) | Gated on prior evidence |

**For agents:** read [`AGENTS.md`](AGENTS.md) and [`RESEARCH-PROMPT.md`](RESEARCH-PROMPT.md). Select one experiment. Use [the model contract](interfaces/model_contract.md), [evaluation contract](interfaces/evaluation_contract.md), and [result template](submissions/TEMPLATE.md). Submit findings as a PR or a stand-alone patch/report.

## Workflow across multiple LLMs

1. Each LLM or researcher claims one experiment using a GitHub issue or a message to the coordinator. Independent duplicate attempts are fine if clearly labeled as replications.
2. It creates a dedicated branch and contributes runnable code, synthetic tests, citations and a precise result note.
3. A reviewer checks causality, licensing, reproducibility and whether a result is measured or merely cited.
4. A separate private integration team may choose to adapt a contribution to its own actual market data and backtesting engine. This public project does **not** contain that data or imply that the public models are profitable.

If a model cannot access GitHub or run code, send it a ZIP snapshot plus an experiment assignment. It can return code patches and a self-contained report using the same interface.

## What counts as progress

A passing smoke test or model checkpoint load is **feasibility**, not trading alpha. A useful contribution may prove that a released checkpoint cannot reproduce its published feature preprocessing from OHLCV, or show that a neural model fails to beat a simple causal baseline. Report both positive and negative evidence and the exact limits of evaluation.

## License and safety

Code is MIT-licensed. Research only; not investment advice. The reference labels are **not** exchange-validated fills, especially for orders touched within a bar. Real assessments require a market-specific fill engine, verified data provenance, leakage-free time splits, transaction costs and risk controls.
