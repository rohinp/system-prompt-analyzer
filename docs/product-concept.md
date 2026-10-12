# Product concept

## The problem

System prompts often grow as unstructured prose. They can sound complete while leaving important
questions unanswered:

- When should a tool be used, and when should it not be used?
- What should happen when a tool fails?
- May the agent take external or irreversible actions without confirmation?
- What prevents the agent from expanding beyond the intended task?
- How should ambiguity, conflicting instructions, and missing information be handled?
- What does a correct final response look like, and when is the work complete?

These omissions are “loose ends.” They are difficult to spot in a long prompt and can cause an
agent to drift, overreach, fabricate, or behave inconsistently.

## The idea

System Prompt Analyzer turns an instruction prompt into two connected views:

1. A map of statements already present in the prompt.
2. A versioned rubric evaluation showing which important controls are present, missing, or not
   relevant to that prompt.

The visual language intentionally distinguishes source material from suggestions. The analyzer
does not claim that every recommendation belongs in every prompt, and it does not rewrite the
prompt without user choice.

## Product principles

- **Evidence before opinion:** present findings quote the prompt and identify line numbers.
- **Explain absence:** missing findings identify the rule that was not satisfied and why it matters.
- **Context matters:** tool, permission, and privacy checks can be not applicable.
- **User control:** recommendations are advisory; future guided editing will require explicit
  acceptance.
- **Stable contracts:** rubric rules and API structures are versioned so evaluations can be
  compared over time.
- **Local first:** the application currently works without an API key and does not persist prompts.

## Intended users

- Developers building tool-using assistants or agents
- Prompt and conversation designers
- AI safety, governance, and quality teams
- Reviewers who need to understand why an agent is allowed to behave in a particular way
- Learners studying system-instruction design

## What the product is not

- A guarantee that an agent is safe or correct
- A replacement for application-level authorization or tool safeguards
- A security scanner for arbitrary code
- A benchmark score that can be compared across unrelated agent types without context
- A model-backed semantic reviewer yet; the current analyzer is deterministic

The analyzer is a design and review aid. Runtime enforcement still belongs in the application,
tool boundary, and authorization system.
