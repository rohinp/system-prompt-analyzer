# Development guide

## Set up

```bash
uv sync
```

`uv.lock` is committed so local development and CI use the same resolved dependency set.

## Run the application

```bash
uv run system-prompt-analyzer
```

The development server reloads when Python files change. Default address:
<http://127.0.0.1:8001>.

## Run checks

```bash
uv run pytest
uv run ruff check .
```

Tests must not call live model providers. External responses will be mocked when provider support
is added.

## Adding or changing a rubric rule

1. Decide whether the change requires a rubric patch, minor, or major version.
2. Add or update the executable definition in `rubric.py`.
3. Add representative positive, missing, and not-applicable examples.
4. Confirm present findings include evidence with correct line numbers.
5. Confirm missing findings include an actionable recommendation.
6. Update `analysis-rubric.md`, `api.md` if needed, and `feature-status.md`.
7. Run all tests and lint checks.

Rule IDs are public identifiers. Do not reuse an old ID for a different meaning.

## Testing strategy

- **Schema tests** protect invariants that every producer must satisfy.
- **Rubric tests** exercise domain examples through the stable `analyze_prompt` boundary.
- **API tests** verify routing, validation, and serialization.
- **Browser tests** will be added when graph interactions become stateful in Increment 4.
- **Evaluation fixtures** will become a scored dataset in Increment 6.

Every confirmed false positive or false negative should become a regression fixture before its
implementation is changed.

## Code conventions

- Python 3.12-compatible syntax
- Type annotations for public functions and structured data
- Pydantic at HTTP and response-contract boundaries
- Domain decisions outside route functions
- Small, explicit modules before generalized frameworks
- Ruff for formatting-related lint, imports, and common correctness checks

## Feature completion checklist

- Observable behavior implemented
- Narrow and full test suites passing
- Lint checks passing
- User workflow manually smoke-tested when the interface changes
- Privacy and failure behavior reviewed
- Relevant documentation updated
- Roadmap increment status updated
