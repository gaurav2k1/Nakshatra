"""PDF rendering of verified chart facts."""

# ruff: noqa: E501

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from nakshatra.charts import BirthChart


def _ascii(value: str) -> str:
    """Normalize known display punctuation for built-in PDF fonts."""
    return value.replace("\u2014", "-").replace("\u2013", "-").replace("\u00b0", " deg")


def render_chart_pdf(chart: BirthChart) -> bytes:
    """Render verified chart facts to a stable, prediction-free PDF report."""
    stream = BytesIO()
    document = SimpleDocTemplate(
        stream,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Nakshatra AI verified chart report",
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#173f36"),
    )
    heading = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#a65d31"),
        spaceBefore=10,
    )
    table_text = ParagraphStyle(
        "TableText",
        parent=styles["BodyText"],
        fontSize=7,
        leading=9,
    )
    story = [
        Paragraph("Nakshatra AI", title),
        Paragraph("Verified Vedic Chart Facts", styles["Heading2"]),
        Spacer(1, 5 * mm),
        Table(
            [
                [
                    "Birth input",
                    f"{chart.birth.date} {chart.birth.time} ({chart.birth.timezone})",
                ],
                [
                    "Coordinates",
                    f"{chart.birth.coordinates.latitude:.4f}, {chart.birth.coordinates.longitude:.4f}",
                ],
                ["UTC instant", chart.utc_datetime.isoformat()],
                ["Julian Day UT", f"{chart.julian_day_ut:.6f}"],
                ["Ayanamsa", f"{chart.ayanamsa} {chart.ayanamsa_degrees:.6f} deg"],
            ],
            colWidths=[42 * mm, 115 * mm],
        ),
        Paragraph("Planetary positions", heading),
        Table(
            [["Graha", "Longitude", "Sign", "House", "Nakshatra", "Motion"]]
            + [
                [
                    p.planet.value.title(),
                    f"{p.longitude:.6f}",
                    p.sign.sign.name.title(),
                    str(p.house),
                    f"{p.nakshatra.nakshatra.value.replace('_', ' ').title()} {p.nakshatra.pada}",
                    "Retrograde" if p.retrograde else "Direct",
                ]
                for p in chart.planets
            ],
            repeatRows=1,
        ),
        PageBreak(),
        Paragraph("Auditable classical rules", heading),
    ]
    for rule in chart.classical_rules:
        story.append(
            Paragraph(
                f"<b>{_ascii(rule.name)}: {'Matched' if rule.present else 'Not matched'}</b><br/>{_ascii(rule.evidence[0])}<br/><font size='8'>{_ascii(rule.source.title)} - {_ascii(rule.source.section)}</font>",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 3 * mm))
    story.extend(
        [
            Paragraph("Planetary dignity", heading),
            Table(
                [["Graha", "Sign", "Status", "Evidence"]]
                + [
                    [
                        d.planet.value.title(),
                        d.sign.name.title(),
                        d.dignity.value.replace("_", " ").title(),
                        Paragraph(_ascii(d.evidence), table_text),
                    ]
                    for d in chart.planetary_dignities
                ],
                repeatRows=1,
                colWidths=[25 * mm, 28 * mm, 30 * mm, 74 * mm],
            ),
            PageBreak(),
            Paragraph("Vimshottari timeline", heading),
        ]
    )
    story.append(
        Table(
            [["Mahadasha", "Start", "End", "Years"]]
            + [
                [
                    p.lord.value.title(),
                    p.start.date().isoformat(),
                    p.end.date().isoformat(),
                    str(p.duration_years),
                ]
                for p in chart.vimshottari_dasha.periods
            ],
            repeatRows=1,
        )
    )
    story.extend(
        [
            Spacer(1, 8 * mm),
            Paragraph("Method note", heading),
            Paragraph(
                "This document contains deterministic calculated facts and explicitly scoped rule checks. It contains no prediction. Lahiri sidereal positions use Swiss Ephemeris; methodology and limitations are documented with the project source.",
                styles["BodyText"],
            ),
        ]
    )

    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173f36")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#aab8b2")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor("#f2f5f3")],
            ),
        ]
    )
    for item in story:
        if isinstance(item, Table):
            item.setStyle(table_style)
    document.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return stream.getvalue()


def _footer(canvas: object, document: SimpleDocTemplate) -> None:
    canvas.saveState()  # type: ignore[attr-defined]
    canvas.setFont("Helvetica", 8)  # type: ignore[attr-defined]
    canvas.setFillColor(colors.HexColor("#65756f"))  # type: ignore[attr-defined]
    canvas.drawString(18 * mm, 10 * mm, "Nakshatra AI - verified facts")  # type: ignore[attr-defined]
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {document.page}")  # type: ignore[attr-defined]
    canvas.restoreState()  # type: ignore[attr-defined]
