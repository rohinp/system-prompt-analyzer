# Getting started

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)

## Install and run

From the repository root:

```bash
uv sync
uv run system-prompt-analyzer
```

Open <http://127.0.0.1:8001>. Interactive API documentation is available at
<http://127.0.0.1:8001/docs>.

The host and port can be changed in a local `.env` file:

```dotenv
APP_HOST=127.0.0.1
APP_PORT=8001
```

## Analyze a prompt

1. Paste a system prompt into the left-hand editor.
2. Select **Analyze prompt**.
3. Read the summary and visual map on the right.
4. Solid nodes represent statements detected in the submitted prompt.
5. Dashed green nodes represent missing rubric controls and suggested additions.

The current implementation runs locally and produces results immediately. No model provider or
API key is required.

## Interpret the result

The response evaluates every rule in rubric version `1.0.0`:

- `present` means matching prompt evidence was detected.
- `missing` means the rule applies, but no matching evidence was detected.
- `not_applicable` means a contextual rule was not triggered. For example, tool-use rules do not
  apply when no tool is mentioned.

The visual map currently shows prompt statements and missing findings. The complete structured
result, including present and not-applicable findings, is available from `POST /api/analyze`.

## Configure a future model provider

Copy the example environment file:

```bash
cp .env.example .env
```

Then set the provider values:

```dotenv
MODEL_PROVIDER=openai
MODEL_NAME=gpt-5-mini
MODEL_API_KEY=your-key
# MODEL_BASE_URL=https://api.openai.com/v1
```

The application does not call a model yet. These values prepare the configuration boundary for
the next roadmap increment. Never commit `.env`.

## Troubleshooting

- **The port is busy:** set `APP_PORT` to another available port in `.env`.
- **Changes do not appear:** the development command enables reload; refresh the browser after the
  server restarts.
- **A finding looks wrong:** deterministic checks currently use explicit textual patterns. See
  [current limitations](analysis-rubric.md#current-limitations).
