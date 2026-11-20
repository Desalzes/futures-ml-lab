# Agent instructions (all coding LLMs)

You are working on a **standalone public** project. Do not look for, infer, request or depend on a private GitHub repository. Read the README, this file, the chosen experiment card, the model interface, and the evaluation contract before coding.

## Objective

Determine whether advanced ML representations can add genuinely useful predictive information to intraday futures **bar-only** trade selection. A high forecast score without net executable improvement is not a trading result. Be willing to return a negative result.

## Selection

If assigned an ID (ML-001 to ML-006), do exactly that. Otherwise select the first open unblocked experiment, checking issue ownership and recent PRs to avoid duplicated efforts. Work on **one experiment per branch/PR**. Before changing any existing interface, explain why compatibility requires it.

## Constraints

- Input only completed OHLCV bars and optional clearly specified bar/calendar covariates. NO L2/L3/order-book/DOM/message data.
- Input features at decision close t may only read bars completed at or before t. Trade fill happens no earlier than the next permitted execution instant.
- Use training-only normalization, causal resampling and purged time-series splits where label windows overlap. Pretraining windows must also be segregated from genuinely unseen evaluations.
- Every model must beat a plain baseline on matched candidate opportunities before an ensemble is justified.
- Do not claim profitability, Topstep pass percentages, checkpoint fidelity or validation without executed evidence.
- Never commit API keys, data, proprietary checkpoint binaries, model weights, or identifying/private project files. Do not place orders, contact brokers or spend money.
- Respect upstream license and checkpoint terms; clearly cite original authors and dates of access in research notes.
- Don't silently optimize thousands of settings on historical years. Prefer a small falsifiable experiment and explain failure.

## Deliverables for a coding-capable agent

- One scoped, runnable module or adapter following interfaces/model_contract.md.
- Synthetic tests including no-lookahead/prefix invariance and ambiguous label handling where applicable.
- Clear installation instructions and dependency versions.
- Research note listing exact upstream commit/checkpoint, input shapes, training/evaluation approach, prerequisites and blockers.
- Verification commands actually executed, and results labeled **synthetic**, **published external evidence**, or **independently tested**.

## Deliverables for a research-only agent

- A detailed design document or source audit for one card, including code entry points, weights/license and tensor schema.
- An implementation-ready handoff and tests a coding agent could write.
- No fabricated test log or profit statistics.

## Contributions

Read CONTRIBUTING.md. Save result notes under submissions/ and general background under research/. Open a draft PR and do not merge without review. If you have no GitHub credentials, provide a patch/ZIP with a summary and the commands needed to verify it.
