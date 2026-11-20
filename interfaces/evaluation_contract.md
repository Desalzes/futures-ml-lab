# Evaluation and evidence standard

## Real experiment admission checks

1. Define the question and **identical candidate opportunity set** before measuring ML lift. A gate that trades 20 cherry-picked cases cannot be compared to a baseline trading 2,000 without reporting selection and uncertainty.
2. Verify vendor timestamps (open vs close labels), timezone, session calendar, CME contract and roll convention, gaps and missing bars. Handle discontinuities instead of blending them into apparent market returns.
3. Features and fitted scalers must be causal. For each model fold, fit preprocessors on that fold's training data only. Do **prefix-invariance tests**: changing later prices must not change the earlier prediction.
4. Train / validation / test are chronological. Purge candidate label look-ahead across split boundaries and embargo overlapping windows. For self-supervised pretraining, restrict pretrained input data to the allowed training chronology.
5. **External pretrained weights:** Record exact checkpoint ID, publication date and *pretraining data period*. Historical periods overlapping external pretraining are not clean unseen evaluations for the full pipeline. When dates are unknown, mark the claim as unverified.
6. Use a plain-feature logistic regression or LightGBM baseline and an un-gated candidate strategy. Test learned embeddings versus an ablated/random embedding control.
7. Evaluate net R with transparent round-trip fees, realistic market-order/stop slippage, adverse gap handling, session flattening and position overlap policy. Stress worse slippage; don't infer guaranteed fills from high/low touches.
8. Report trade count, net expectancy (with uncertainty), distribution by time block, profit concentration, max drawdown, calibration, cost sensitivity, and for any prop simulation, **finished, failed and unresolved** evaluation counts with correctly dated rules.

## Progressive research stages

- **Stage A:** source/weights/license + feature schema audit (no claims about performance).
- **Stage B:** synthetic input and timestamp tests; reproduction of upstream inference.
- **Stage C:** matched baseline and trained model on *legitimate locally held data* using walk-forward or expanding-window evaluation.
- **Stage D:** truly prospective/outside-pretraining paper evaluation, after costs, with explicit uncertainty.

This public repo intentionally supplies only Stage A/B examples. A contributor cannot claim C/D from synthetic data. Never generate made-up trades or returns in a report.

## Stop early if

Data feature schema is incompatible; checkpoint access or license fails; leakage cannot be ruled out; lift disappears against the baseline; performance depends on one exceptional regime; increased slippage eliminates the benefit; or selected trade count is too small to support the claimed effect.
