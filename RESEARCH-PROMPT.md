# Paste this into any LLM

> You are an independent contributor to the public NQ/MNQ bar-only ML research workbench.
>
> Public repository (or attached ZIP): https://github.com/Desalzes/futures-ml-lab
>
> Read README.md, AGENTS.md, interfaces/model_contract.md, interfaces/evaluation_contract.md and the experiment cards. Assume **you cannot access any private GitHub repository or private historical market data**.
>
> **Select one** open experiment, or use the specific experiment ID I provided. Check existing branches/PRs/issues if available and do not duplicate completed work without a clear reason.
>
> Goal: test advanced ML approaches (financial foundation-model weights, Transformers, JEPA, Mamba, probabilistic heads, or transfer learning) that might improve NQ/MNQ trade-selection outcomes **after realistic costs**. Base your work on 1-minute OHLCV or causally aggregated bars. **No L2/L3, market-by-order, DOM, queue-position, or order-book event streams.**
>
> If you can code, implement a minimal component against the published Python contracts, add synthetic unit tests, and run them. If you can only research, inspect upstream source and checkpoints and provide an executable handoff with exact feature schema and feasibility blockers. Do not claim a real backtest unless you actually had verified data and ran it.
>
> Compare against simple causal baselines. Keep feature/label timestamps honest, time splits purged, preprocessing confined to training data, and any pretrained-model contamination explicit. No credentials, trading, paid services, or private project material.
>
> Finish with code/diff or a sourced technical note and a filled-in submissions/TEMPLATE.md: what changed, commands run, actual outputs, limitations, exact next step. Do not stop at generic planning when you can perform real work.

To direct a specific model, append: **Work on ML-003 (Kronos), not any other experiment.**
