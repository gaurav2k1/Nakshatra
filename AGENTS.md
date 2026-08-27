# Nakshatra AI Project Instructions

## Project identity

- Project: Nakshatra AI
- Tagline: Explainable AI powered Vedic Astrology Platform
- Canonical local checkout: `D:\Code\Nakshatra`
- Treat this repository as a production-grade, long-lived open-source project.

## Required project context

Before designing, implementing, reviewing, or testing Nakshatra AI, read
[`docs/MASTER_DEVELOPMENT_PROMPT.md`](docs/MASTER_DEVELOPMENT_PROMPT.md). It is
the authoritative development brief and defines the architecture, engineering
standards, deterministic-calculation boundary, testing expectations, and
milestone scope.

Apply that brief to repository work while preserving the user's current request
and the actual state of the codebase. Do not infer permission for unrelated
changes, releases, commits, or external side effects.

## Non-negotiable product rules

- Astrology and astronomy calculations must be deterministic and verifiable.
- AI may explain verified facts; AI must not perform astrological calculations.
- Match Swiss Ephemeris within explicitly documented tolerances.
- Cite sources for mathematical transformations and implemented astrological
  rules.
- Use production-quality implementations: no placeholders, toy code, TODOs, or
  silent fallbacks.
- Keep modules independently testable and avoid global mutable state, circular
  imports, and god classes.
- For implementation work, update relevant tests and documentation, and run the
  applicable quality checks before reporting completion.
- Do not expand beyond the active milestone unless the user explicitly asks.

