# P.A.U.L.I.
Patient-centered AI for Understanding Literature and Insights

## App runtime: user-configured Ollama (local or cloud)

The app talks directly to Ollama (via `ollama-python`).
The user chooses local models (private, no key) or Ollama cloud models
(requires an API key).

- `OLLAMA_HOST` (default `http://localhost:11434`; point it at the Ollama
  cloud endpoint to use cloud models), `OLLAMA_CHAT_MODEL`,
  `OLLAMA_EMBED_MODEL` (default `nomic-embed-text`).
- `OLLAMA_API_KEY` only for Ollama cloud; empty for local. Set it in the
  environment or a local `.env` file (gitignored). Never logged or committed.

## UI tests (python-playwright + pytest-playwright)

UI tests live in `tests/ui/` and run against the static `ui-mockup/`.

```bash
poetry install --with dev --no-root
poetry run python -m playwright install chromium
poetry run pytest tests/ui -v
```

## Development tooling (dev-only)

`setup_dev_ai.sh` is only for developing this project. It installs Ollama +
an opencode coding agent with a local model. The app itself does not use it —
in particular the app never uses the `ollama launch opencode` harness.

```bash
./setup_dev_ai.sh
```

**Note**: The `MODEL` variable in `setup_dev_ai.sh` configures only the
dev coding agent. It is not read by the app.