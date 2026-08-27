# Changelog

All notable changes to this project will be documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-08-27

### Added

- Hostable FastAPI application with OpenAPI and ReDoc documentation.
- Versioned `POST /api/v1/charts` deterministic calculation endpoint.
- Liveness and readiness health endpoints.
- Responsive birth-detail and verified planetary-results browser interface.
- Same-origin browser client with actionable validation errors.
- Conservative browser security headers.
- Production Dockerfile running as an unprivileged user.
- API integration tests.

## [0.1.0] - 2026-08-27

### Added

- Python packaging and quality-tool configuration.
- Immutable, validated birth input and coordinate models.
- IANA timezone conversion with explicit DST gap and overlap detection.
- Deterministic Julian Day calculation based on Meeus chapter 7.
- Initial `version` and `info` CLI commands.
- Thread-safe Swiss Ephemeris wrapper using Lahiri sidereal mode.
- Planet models and deterministic positions for nine Vedic grahas.
- Zodiac sign calculation with property-based boundary tests.
- Birth-chart orchestration and JSON generation.
- `generate`, `doctor`, and `validate` CLI commands.
- Runtime diagnostics for Python, Swiss Ephemeris, timezone data, ephemeris
  configuration, calculations, ranges, and serialization.
- J2000 Lahiri golden-reference regression fixture with one-arc-second
  tolerance.
- Unit tests and project documentation.
