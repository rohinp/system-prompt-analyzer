# ADR-0002: Keep prompts ephemeral by default

- Status: Accepted
- Date: 2026-10-12

## Context

System prompts may contain proprietary policies, tool details, or sensitive operational context.
Persistence introduces access control, retention, deletion, encryption, and breach-response duties.

## Decision

Do not persist submitted prompts or analysis results in the initial product. Keep provider secrets
in server-side environment configuration and never return them to the browser.

## Consequences

- Local use has a small privacy and operational footprint.
- Users must resubmit prompts after a page or server restart.
- Saved analyses, history, accounts, and collaboration require an explicit future design and
  migration rather than an accidental database addition.
