# Changelog

All notable changes to this project will be documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.8.0] - 2026-08-27

### Added

- Directed whole-sign Graha Drishti between calculated chart placements.
- Universal seventh and special Mars, Jupiter, and Saturn full aspects.
- Explicit source and geometric evidence for each returned aspect.
- Aspect validation, API coverage, focused tests, and browser presentation.

## [0.7.0] - 2026-08-27

### Added

- Deterministic exalted, debilitated, own-sign, and neutral classifications.
- Deep exaltation and debilitation degree metadata for seven visible grahas.
- Explicit non-evaluation of disputed Rahu and Ketu dignities.
- Source-scoped evidence in chart JSON, validation, tests, and browser UI.

## [0.6.0] - 2026-08-27

### Added

- Pure, deterministic evaluation for three explicitly scoped classical rules.
- Budha-Aditya same-sign conjunction audit.
- Structural Gajakesari Moon/Jupiter Kendra audit.
- Five-house Lagna variant of Mangala Dosha audit.
- Evidence and source metadata for every matched and unmatched result.
- Browser evidence cards plus API, validation, and regression coverage.

## [0.5.0] - 2026-08-27

### Added

- Deterministic Vimshottari Mahadasha lord and birth-balance calculation.
- Complete contiguous nine-lord, 120-year Mahadasha cycle.
- Explicit 365.25-day Dasha-year conversion convention.
- Vimshottari output in the CLI and versioned chart API.
- Browser timeline with active-at-birth period and remaining balance.
- Boundary, continuity, duration, validation, and golden-reference tests.

## [0.4.0] - 2026-08-27

### Added

- Reusable deterministic divisional-chart transformation engine.
- D1 Rāśi positions for the Ascendant and all supported grahas.
- D9 Navāṁśa positions and divisional whole-sign house assignments.
- D1/D9 output in the CLI and versioned chart API.
- Interactive Rāśi/Navāṁśa switching for North and South Indian views.
- Property-based Navāṁśa boundary and normalization tests.
- Divisional-chart installation validation and golden reference fields.

## [0.3.0] - 2026-08-27

### Added

- Lahiri sidereal Ascendant calculation through Swiss Ephemeris.
- Twelve whole-sign house cusps and deterministic planetary house assignment.
- All 27 Nakshatras with four-Pada calculation and property-based tests.
- Enriched API and JSON chart output containing houses and Nakshatra positions.
- Responsive North Indian house and South Indian sign chart views.
- Expanded installation validation and J2000 golden reference data.

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
