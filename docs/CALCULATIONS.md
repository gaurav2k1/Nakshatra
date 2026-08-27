# v0.1 Calculation Methodology

## Time conversion

Birth input uses a civil date and time plus an IANA timezone name. Nakshatra
converts this to UTC with Python's `zoneinfo` database. It tests both PEP 495
fold values by round-tripping through UTC, rejecting nonexistent DST times and
ambiguous repeated times rather than guessing an instant.

## Julian Day

Julian Day follows Jean Meeus, *Astronomical Algorithms*, second edition,
chapter 7. Inputs are converted to UTC first. Python uses the proleptic
Gregorian calendar, so this implementation does the same.

The J2000 reference instant `2000-01-01T12:00:00Z` must produce Julian Day
`2451545.0`.

## Planet positions

Positions are calculated with pyswisseph 2.10 using `swe_calc_ut` and these
flags:

- Swiss Ephemeris requested
- Speed requested
- Sidereal positions requested

The sidereal mode is Lahiri. Results are apparent geocentric ecliptic
longitudes. The engine currently calculates Sun, Moon, Mercury, Venus, Mars,
Jupiter, Saturn, and the mean lunar ascending node (Rahu). Ketu is derived at
exactly 180° from Rahu. Retrograde state is determined from the sign of
longitudinal speed.

Swiss Ephemeris configuration is process-global. The integration serializes
configuration and calculations with a reentrant lock and reapplies Lahiri mode
for every request, preventing concurrent callers from changing the result.

When `NAKSHATRA_EPHEMERIS_PATH` is unset or the requested Swiss data files are
unavailable, the underlying library may use its built-in Moshier ephemeris.
Production deployments requiring Swiss `.se1` files should configure the path
and verify it with `nakshatra doctor`.

## Signs

Longitudes are normalized to `[0°, 360°)`. The sidereal zodiac consists of
twelve equal 30° signs beginning with Aries at 0°. Sign calculation is a direct
deterministic partition; it does not involve AI interpretation.

## Ascendant and houses

The sidereal Ascendant is calculated with Swiss Ephemeris `swe_houses_ex` at
the UT Julian Day and geographic coordinates, using the Lahiri sidereal mode.
Nakshatra AI v0.3 uses whole-sign houses: the Ascendant's sign is house one and
each subsequent 30-degree sign is the next house. Cusps therefore lie on exact
sign boundaries. Planetary house assignment is derived from the difference
between the planet's sign index and Ascendant sign index.

## Nakshatras and Padas

The 360-degree sidereal zodiac is divided into 27 equal Nakshatras of 13
degrees 20 arcminutes, beginning with Ashwini at 0 degrees Aries. Each
Nakshatra contains four equal Padas of 3 degrees 20 arcminutes. Boundary and
normalization behavior is covered by property-based tests.

## Golden tolerance

The J2000 Lahiri fixture records expected values produced by Swiss Ephemeris.
Regression comparisons use an absolute tolerance of one arc second
(`1 / 3600` degree). Ketu's opposition to Rahu is verified independently.

## Divisional charts

D1 Rāśi preserves the natal sidereal sign and degrees within that sign.

D9 Navāṁśa divides the zodiac into 108 equal portions of 3 degrees 20
arcminutes. Beginning from Aries, Navāṁśa signs repeat through the twelve-sign
sequence. The transformation is therefore equivalent to multiplying the
normalized sidereal longitude by nine and normalizing it to 360 degrees. The
same transformation is applied to the Ascendant and every graha, after which
whole-sign houses are assigned relative to the divisional Ascendant.

This construction follows the classical Varga scheme described in Brihat
Parashara Hora Shastra's treatment of divisional charts. The implementation is
a pure numerical transformation and does not attach interpretive claims.

## Vimshottari Mahadasha

The birth Mahadasha is selected from the Moon's sidereal Nakshatra. The
sequence of lords and traditional lengths is Ketu 7, Venus 20, Sun 6, Moon 10,
Mars 7, Rahu 18, Jupiter 16, Saturn 19, and Mercury 17 years, totaling 120
years. The sequence repeats every nine Nakshatras beginning with Ashwini ruled
by Ketu.

The fraction of the birth Mahadasha already elapsed is the Moon's degrees
traversed within its Nakshatra divided by 13 degrees 20 arcminutes. The balance
is the complementary fraction multiplied by that lord's period length.

Nakshatra AI converts traditional Dasha years to timestamps using an explicit
365.25-day year. This is a documented computational convention rather than a
claim that a Dasha year equals a civil calendar year. The sequence follows the
Vimshottari scheme described in Brihat Parashara Hora Shastra. v0.5 calculates
Mahadasha periods only; Antardasha subdivisions and interpretations are outside
this milestone.
