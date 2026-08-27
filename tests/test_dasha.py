from datetime import UTC, datetime

import pytest

from nakshatra.astrology.dasha import VIMSHOTTARI_YEAR_DAYS, vimshottari_dasha
from nakshatra.astrology.nakshatras import nakshatra_position
from nakshatra.planets import Planet

BIRTH = datetime(2000, 1, 1, 12, tzinfo=UTC)


def test_ashwini_begins_with_complete_ketu_mahadasha() -> None:
    result = vimshottari_dasha(BIRTH, nakshatra_position(0))

    assert result.birth_lord is Planet.KETU
    assert result.balance_years == pytest.approx(7)
    assert result.periods[0].start == BIRTH
    assert (
        result.periods[0].end - result.periods[0].start
    ).total_seconds() == pytest.approx(7 * VIMSHOTTARI_YEAR_DAYS * 86_400)


def test_halfway_through_bharani_leaves_half_of_venus_period() -> None:
    result = vimshottari_dasha(BIRTH, nakshatra_position(20))

    assert result.birth_lord is Planet.VENUS
    assert result.elapsed_fraction == pytest.approx(0.5)
    assert result.balance_years == pytest.approx(10)
    assert result.periods[0].start < BIRTH < result.periods[0].end


def test_cycle_is_contiguous_and_totals_120_years() -> None:
    result = vimshottari_dasha(BIRTH, nakshatra_position(199.47055295238044))

    assert len(result.periods) == 9
    assert result.birth_lord is Planet.RAHU
    assert all(
        first.end == second.start
        for first, second in zip(result.periods[:-1], result.periods[1:], strict=True)
    )
    total_days = (
        result.periods[-1].end - result.periods[0].start
    ).total_seconds() / 86_400
    assert total_days == pytest.approx(120 * VIMSHOTTARI_YEAR_DAYS)
    for mahadasha in result.periods:
        assert len(mahadasha.antardashas) == 9
        assert mahadasha.antardashas[0].lord is mahadasha.lord
        assert mahadasha.antardashas[0].start == mahadasha.start
        assert mahadasha.antardashas[-1].end == mahadasha.end
        assert all(
            first.end == second.start
            for first, second in zip(
                mahadasha.antardashas[:-1],
                mahadasha.antardashas[1:],
                strict=True,
            )
        )


def test_antardasha_lengths_are_proportional_to_lord_years() -> None:
    result = vimshottari_dasha(BIRTH, nakshatra_position(0))
    ketu_mahadasha = result.periods[0]

    assert ketu_mahadasha.antardashas[0].duration_years == pytest.approx(7 * 7 / 120)
    assert ketu_mahadasha.antardashas[1].duration_years == pytest.approx(7 * 20 / 120)


def test_dasha_requires_timezone_aware_birth_instant() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        vimshottari_dasha(
            datetime(2000, 1, 1, 12),
            nakshatra_position(0),
        )
