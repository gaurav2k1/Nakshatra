"""Nakshatra AI command-line interface."""

from datetime import date as Date
from datetime import time as Time
from typing import Annotated

import typer

from nakshatra import __version__
from nakshatra.charts import generate_chart
from nakshatra.models import BirthInput, Coordinates
from nakshatra.validation import ValidationReport, doctor, validate_installation

app = typer.Typer(no_args_is_help=True, help="Nakshatra AI deterministic engine")


@app.command()
def version() -> None:
    """Display the installed Nakshatra AI version."""
    typer.echo(f"Nakshatra AI {__version__}")


@app.command()
def info() -> None:
    """Describe the engine's calculation boundary."""
    typer.echo(
        "Nakshatra AI uses deterministic astronomy and astrology calculations; "
        "AI is reserved for explaining verified facts."
    )


def _print_report(report: ValidationReport) -> None:
    for check in report.checks:
        typer.echo(f"{check.status.value:<4} {check.name}: {check.detail}")
    if not report.ok:
        raise typer.Exit(code=1)


@app.command(name="doctor")
def doctor_command() -> None:
    """Check the runtime and calculation dependencies."""
    _print_report(doctor())


@app.command(name="validate")
def validate_command() -> None:
    """Run deterministic installation integrity checks."""
    _print_report(validate_installation())


@app.command()
def generate(
    date: Annotated[str, typer.Option(help="Civil date in YYYY-MM-DD format")],
    time: Annotated[str, typer.Option(help="Civil time in HH:MM[:SS] format")],
    timezone: Annotated[str, typer.Option(help="IANA timezone, such as Asia/Kolkata")],
    latitude: Annotated[float, typer.Option(min=-90.0, max=90.0)],
    longitude: Annotated[float, typer.Option(min=-180.0, max=180.0)],
) -> None:
    """Generate deterministic v0.1 birth-chart facts as JSON."""
    birth = BirthInput(
        date=Date.fromisoformat(date),
        time=Time.fromisoformat(time),
        timezone=timezone,
        coordinates=Coordinates(latitude=latitude, longitude=longitude),
    )
    typer.echo(generate_chart(birth).model_dump_json(indent=2))


if __name__ == "__main__":
    app()
