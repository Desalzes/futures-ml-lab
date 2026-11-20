# Publish this standalone ZIP as a new public repository

The GitHub connector used to prepare this project can write to **existing** repositories but cannot create a new one. Publishing is therefore a one-time manual action through GitHub or GitHub CLI. **Do not publish by copying a private repository or its git history.** This folder contains its own clean source tree.

## Fastest path with GitHub CLI

1. Unzip `futures-ml-lab.zip` and open a terminal inside the extracted `futures-ml-lab` directory.
2. Inspect the files and confirm they contain no sensitive material.
3. Run `bash scripts/publish_public.sh --confirm-public` while logged into `gh auth login` as the intended account.
4. Verify the repository is marked **Public**, run its Actions tests, and share its URL with other LLMs.

The publishing script checks that the directory has no inherited `.git`, requires the explicit public confirmation flag, initializes new history and calls `gh repo create Desalzes/futures-ml-lab --public --source=. --remote=origin --push`.

## Website-only alternative

1. Open https://github.com/new and create `futures-ml-lab` under account `Desalzes`, visibility **Public**, with **no starter README or .gitignore**.
2. In the extracted folder:

```bash
git init -b main
git add .
git commit -m "Initial public bar-only ML research lab"
git remote add origin https://github.com/Desalzes/futures-ml-lab.git
git push -u origin main
```

3. Check https://github.com/Desalzes/futures-ml-lab and run the synthetic unit tests on Actions.

If you choose another account or repo name, replace the owner/name in RESEARCH-PROMPT.md and the publication script before publishing.

## Redaction policy

Do not copy upstream private git history, proprietary strategies, exact internal performance figures, trade logs, historical bar files, model weights, credentials or private paths to this repo. The cards and sample code were independently written for this public template; nothing requires a private project.
