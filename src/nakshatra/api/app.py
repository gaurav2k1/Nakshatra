"""FastAPI application and local server entry point."""

from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nakshatra import __version__
from nakshatra.charts import BirthChart, generate_chart
from nakshatra.models import BirthInput
from nakshatra.validation import doctor

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent
_templates = Jinja2Templates(directory=_PACKAGE_ROOT / "templates")

app = FastAPI(
    title="Nakshatra AI",
    summary="Deterministic Vedic astrology calculations",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
app.mount(
    "/static",
    StaticFiles(directory=_PACKAGE_ROOT / "static"),
    name="static",
)


@app.middleware("http")
async def security_headers(request: Request, call_next: Any) -> Any:
    """Attach conservative browser security headers to every response."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request) -> HTMLResponse:
    """Render the interactive birth-chart workspace."""
    return _templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"version": __version__},
    )


@app.get("/health/live", tags=["health"])
def live() -> dict[str, str]:
    """Report that the web process is accepting requests."""
    return {"status": "ok", "version": __version__}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    """Report whether deterministic runtime dependencies are ready."""
    report = doctor()
    return {"status": "ready" if report.ok else "unavailable"}


@app.post("/api/v1/charts", response_model=BirthChart, tags=["charts"])
def create_chart(birth: BirthInput) -> BirthChart:
    """Calculate verified v0.2 chart facts from validated birth input."""
    return generate_chart(birth)


def run() -> None:
    """Run the development server on localhost."""
    uvicorn.run("nakshatra.api.app:app", host="127.0.0.1", port=8000, reload=False)
