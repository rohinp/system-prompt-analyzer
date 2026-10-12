# Privacy and security

## Current data flow

Prompt text travels from the browser to the local FastAPI process over the configured HTTP
connection. The deterministic analyzer evaluates it in memory and returns a structured response.

The project currently:

- does not store prompts in a database or file;
- does not send prompts to a model provider;
- does not include analytics or telemetry;
- does not return API-key values to the browser;
- renders user and analysis text through DOM `textContent`, not HTML insertion.

## API keys

Model credentials will be read from `MODEL_API_KEY` in the environment or local `.env` file.
`.env` is ignored by Git. `.env.example` contains names only and must never contain a real key.

Provider support is not implemented yet, so configuring a key currently changes only the status
indicator.

## Trust boundaries

- Submitted prompts are untrusted data, not instructions for the analyzer runtime.
- Future model output will also be treated as untrusted and validated against the Pydantic schema.
- Prompt guidance cannot replace code-level permissions on tools and external actions.
- The public configuration endpoint exposes only provider name, model name, and whether a key is
  configured.

## Deployment considerations

The no-persistence guarantee covers application code. A production operator must separately
configure reverse proxies, platform logs, request tracing, crash reporting, and backups so they do
not capture prompt bodies or secrets.

Before public deployment, roadmap Increment 7 adds request limits, redacted structured logging,
secure headers, readiness checks, and documented retention policy.

## Reporting a concern

Do not include real credentials or sensitive prompt contents in an issue report. Provide the
smallest synthetic example that reproduces the problem.
