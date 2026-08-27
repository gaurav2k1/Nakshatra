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

## Classical rule audit

Version 0.6 evaluates three deliberately narrow, deterministic placement
rules. A result is an auditable condition check, not a prediction or a complete
traditional interpretation.

- **Budha-Aditya Yoga:** matched when the Sun and Mercury occupy the same
  sidereal sign. The source label identifies the Budha-Aditya entry in the
  classical Yoga catalogue attributed to *Brihat Parashara Hora Shastra*.
- **Gajakesari Yoga (structural condition):** matched when Jupiter is in house
  1, 4, 7, or 10 counted inclusively from the Moon's sign. Classical texts add
  strength and affliction qualifications; v0.6 intentionally reports only the
  geometric Kendra condition and says so in the source scope.
- **Mangala Dosha (five-house Lagna variant):** matched when Mars occupies
  whole-sign house 1, 4, 7, 8, or 12 from the Ascendant. The source label is
  *Phaladeepika*, chapter 7. Alternate reference points, regional variants,
  exceptions, and cancellation rules are outside this implementation.

Each API result contains the stable rule identifier, category, matched state,
human-readable placement evidence, and source metadata. Negative results also
retain evidence so callers can verify why a condition did not match.

## Planetary dignity

Version 0.7 classifies the seven visible grahas by sidereal sign as exalted,
debilitated, in an own sign, or neutral. The exaltation signs and deepest
degrees follow *Brihat Parashara Hora Shastra*, chapter 3, verses 49-50:
Sun Aries 10°, Moon Taurus 3°, Mars Capricorn 28°, Mercury Virgo 15°,
Jupiter Cancer 5°, Venus Pisces 27°, and Saturn Libra 20°. Debilitation is the
opposite sign at the same degree. Sign rulership in the same chapter supplies
the own-sign classification. When Mercury is in Virgo, exaltation takes
precedence over the overlapping own-sign label.

Rahu and Ketu return `not_evaluated`. Classical authorities disagree about
node exaltation and debilitation, as noted in *Phaladeepika* chapter 1, so the
engine does not silently choose a disputed convention. This milestone reports
sign-level status and reference degrees only; it does not calculate Shadbala,
friend/enemy dignity, Moolatrikona boundaries, cancellation, or predictions.

## Graha Drishti

Version 0.8 calculates directed full aspects by inclusive forward sign count.
All seven visible grahas cast a full seventh aspect. Mars additionally casts
full fourth and eighth aspects, Jupiter fifth and ninth aspects, and Saturn
third and tenth aspects. This scope follows *Brihat Parashara Hora Shastra*,
chapter 27, verse 3.

Each result identifies the aspecting and aspected graha, relative sign number,
whether it is special, geometric evidence, and the source. Rahu and Ketu may
receive aspects but do not cast them in v0.8 because node-aspect conventions
vary. Partial aspect strength, orb-based aspects, Rashi Drishti, effects, and
interpretation are outside this milestone.

## Expanded Yoga catalogue

Version 0.9 adds the solar Yogas described in *Brihat Parashara Hora Shastra*,
chapter 37. Among Mars, Mercury, Jupiter, Venus, and Saturn, occupancy of only
the second sign from the Sun yields Vesi, only the twelfth yields Vosi, and
occupancy on both sides yields Ubhayachari. The engine reports these three as
mutually exclusive and excludes the Moon and lunar nodes.

The same chapter's verse 5 supplies the Adhi Yoga geometry. Nakshatra uses the
strict, fully auditable form: Mercury, Jupiter, and Venus must collectively
occupy all three of the sixth, seventh, and eighth signs from the Moon. It does
not label one- or two-position variants as full Adhi Yoga and does not infer
the text's promised effects or grade planetary strength.

## Vimshottari Antardasha

Version 0.10 subdivides each Mahadasha into nine Antardashas. The sub-period
sequence begins with the Mahadasha lord and follows the same repeating lord
order. For Mahadasha lord `M` and Antardasha lord `A`, the duration is
`years(M) × years(A) / 120`. The existing explicit 365.25-day year converts
that duration to timestamps.

Tests verify that each group starts and ends exactly on its parent Mahadasha
boundaries, contains nine contiguous sub-periods, and preserves the classical
proportions. Pratyantardasha and interpretive effects remain outside v0.10.
