# Contributing

This public lab is designed for independent, reproducible contributions from humans and multiple LLMs. **One experiment per PR** and one issue claim per active contribution. An issue claim is coordination, not an exclusive lock.

1. Read AGENTS.md and the assigned experiments/ML-XXX.md file.
2. Open an issue using the experiment template; label the branch `ml-XXX-short-purpose`.
3. Cite upstream source URLs, revisions and licenses. Never copy unlicensed weights/data into the repository.
4. Keep model adapters isolated (for example `src/futures_ml_lab/experiments/ml_003_kronos.py`) and use existing Bar/FeatureRow/Candidate structures. If an advanced architecture needs an optional package, put it in a separately documented optional dependency, not the core harness.
5. Add synthetic tests; make causality and timestamp assumptions explicit.
6. Run `python -m unittest discover -s tests -v`; note anything unavailable.
7. Commit a concise submissions/ML-XXX-your-topic.md following TEMPLATE.md and open a draft PR.

Real-market results, if ever independently provided, must document lawful data provenance, license, date ranges, exact contract handling, economic assumptions and overlap with pretraining. No uploading restricted market bars. A published paper's metric is not an independent result.

## Rejections and negative results

A reproducible failure is valuable. Keep the result note even if the implementation is rejected. Do not conceal that a large model underperformed a logistic/LightGBM baseline.

## Security and privacy

Never copy work from a private repo into this public repo without an explicit release review. Do not submit account numbers, trade credentials, API keys, unreleased strategies, proprietary datasets or raw fills. Use only synthetic fixtures in tests. Respect no-broker/no-execution boundaries.
