# Nakshatra AI

Explainable AI powered Vedic Astrology Platform.

Nakshatra AI is building a deterministic, mathematically verifiable Vedic
astrology engine. Astronomical and astrological facts are computed in code;
AI is reserved for explaining already-verified results.

## Current milestone: v0.4

The fourth milestone adds deterministic D1 Rāśi and D9 Navāṁśa charts for the
Ascendant and all nine grahas. Both divisional charts can be explored in North
and South Indian browser views. The web layer displays verified chart facts;
it does not add predictions or AI calculations.

The v0.1 deterministic vertical slice now includes validated inputs,
timezone-safe UTC conversion, Julian Day calculation, Lahiri sidereal planetary
positions, zodiac signs, JSON output, runtime diagnostics, and golden-reference
tests.

## Development

Python 3.12 or newer and [uv](https://docs.astral.sh/uv/) are recommended.

```console
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run mypy
```

## CLI

```console
uv run nakshatra version
uv run nakshatra info
uv run nakshatra doctor
uv run nakshatra validate
uv run nakshatra generate --date 2000-01-01 --time 17:30:00 \
  --timezone Asia/Kolkata --latitude 13.0827 --longitude 80.2707
```

## Web application

Run the local hostable service:

```console
uv run nakshatra-web
```

Open `http://127.0.0.1:8000` for the browser interface or
`http://127.0.0.1:8000/api/docs` for interactive API documentation.

The versioned calculation endpoint is `POST /api/v1/charts`. Operational probes
are available at `GET /health/live` and `GET /health/ready`.

Build and run the production container with:

```console
docker build -t nakshatra-ai:0.4.0 .
docker run --rm -p 8000:8000 nakshatra-ai:0.4.0
```

`generate` emits machine-readable JSON containing the normalized UTC instant,
UT Julian Day, Lahiri ayanamsa, and positions for Sun, Moon, Mercury, Venus,
Mars, Jupiter, Saturn, mean Rahu, and Ketu. Ketu is calculated exactly 180°
opposite Rahu.

Set `NAKSHATRA_EPHEMERIS_PATH` to a Swiss Ephemeris data directory when using
external `.se1` files. Without it, pyswisseph uses its built-in Moshier
ephemeris fallback. Run `nakshatra doctor` to see which configuration is active.

## Calculation references

The Julian Day implementation follows Jean Meeus, *Astronomical Algorithms*,
2nd edition, chapter 7. Each future mathematical transformation and classical
astrological rule will carry an equivalent source citation.

See [Calculation methodology](docs/CALCULATIONS.md) for the precise v0.1
ephemeris contract and validation tolerance.

## License

MIT
