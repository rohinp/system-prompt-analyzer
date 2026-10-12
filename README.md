# System Prompt Analyzer

Turn a system prompt into an interactive map of its instructions, constraints, guards,
tool-use rules, and potential gaps.

See the [project documentation](docs/README.md) for user and technical guides, and the
[incremental delivery plan](PLAN.md) for the path to a model-backed production release.

The current application includes a FastAPI backend, responsive web interface, versioned formal
analysis rubric, structured evidence-backed findings, provider configuration, and automated tests.
A model-backed analyzer can be added behind the same `/api/analyze` contract without rewriting the
interface.

## Documentation

- [Getting started](docs/getting-started.md)
- [Product concept](docs/product-concept.md)
- [Understanding results](docs/concepts.md)
- [Analysis rubric](docs/analysis-rubric.md)
- [API contract](docs/api.md)
- [Architecture](docs/architecture.md)
- [Development guide](docs/development.md)
- [Privacy and security](docs/privacy-and-security.md)

## Run locally

```bash
uv sync
uv run system-prompt-analyzer
```

Open <http://127.0.0.1:8001>. API documentation is available at
<http://127.0.0.1:8001/docs>. The port can be changed with `APP_PORT` in `.env`.

## Configure a model provider

The scaffold does not call a model yet, so an API key is optional. To prepare local
configuration:

```bash
cp .env.example .env
```

Set `MODEL_API_KEY` in `.env`. `MODEL_PROVIDER`, `MODEL_NAME`, and `MODEL_BASE_URL` make it
possible to add an OpenAI-compatible provider in the next increment. Never commit `.env`.

## Quality checks

```bash
uv run pytest
uv run ruff check .
```
