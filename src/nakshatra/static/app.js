const form = document.querySelector("#birth-form");
const emptyState = document.querySelector("#empty-state");
const results = document.querySelector("#results");
const errorBox = document.querySelector("#error");
const planetGrid = document.querySelector("#planet-grid");
const submitButton = form.querySelector("button[type='submit']");
const kundliChart = document.querySelector("#kundli-chart");
const chartTabs = document.querySelectorAll(".chart-tab");
const divisionTabs = document.querySelectorAll(".division-tab");
let currentChart = null;

const signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
const glyphs = { sun: "☉", moon: "☾", mercury: "☿", venus: "♀", mars: "♂", jupiter: "♃", saturn: "♄", rahu: "☊", ketu: "☋" };

const degrees = (value) => `${value.toFixed(4)}°`;

chartTabs.forEach((tab) => tab.addEventListener("click", () => {
  chartTabs.forEach((item) => item.classList.toggle("active", item === tab));
  kundliChart.className = `kundli-chart ${tab.dataset.chart}`;
  if (currentChart) renderKundli(currentChart, tab.dataset.chart);
}));

divisionTabs.forEach((tab) => tab.addEventListener("click", () => {
  divisionTabs.forEach((item) => item.classList.toggle("active", item === tab));
  if (currentChart) renderKundli(currentChart, document.querySelector(".chart-tab.active").dataset.chart);
}));

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.hidden = true;
  submitButton.disabled = true;
  submitButton.firstElementChild.textContent = "Calculating…";
  const data = new FormData(form);
  const payload = {
    date: data.get("date"),
    time: data.get("time"),
    timezone: data.get("timezone"),
    coordinates: {
      latitude: Number(data.get("latitude")),
      longitude: Number(data.get("longitude")),
    },
  };

  try {
    const response = await fetch("/api/v1/charts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const problem = await response.json();
      throw new Error(problem.detail?.[0]?.msg || "The chart could not be calculated.");
    }
    renderChart(await response.json());
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.hidden = false;
  } finally {
    submitButton.disabled = false;
    submitButton.firstElementChild.textContent = "Generate verified chart";
  }
});

function renderChart(chart) {
  currentChart = chart;
  document.querySelector("#utc").textContent = chart.utc_datetime.replace("T", " ");
  document.querySelector("#jd").textContent = chart.julian_day_ut.toFixed(6);
  document.querySelector("#ayanamsa").textContent = `${chart.ayanamsa} ${degrees(chart.ayanamsa_degrees)}`;
  renderKundli(chart, document.querySelector(".chart-tab.active").dataset.chart);
  renderDasha(chart.vimshottari_dasha);
  renderRules(chart.classical_rules);
  planetGrid.replaceChildren(...chart.planets.map((planet) => {
    const item = document.createElement("article");
    item.className = "planet";
    item.innerHTML = `<span class="glyph">${glyphs[planet.planet]}</span><div><strong>${planet.planet}</strong><span>${signs[planet.sign.sign]} · ${degrees(planet.sign.degrees_in_sign)}</span></div><b>${planet.retrograde ? "℞" : "Direct"}</b>`;
    return item;
  }));
  emptyState.hidden = true;
  results.hidden = false;
}

function renderKundli(chart, style) {
  const divisionName = document.querySelector(".division-tab.active").dataset.division;
  const division = chart.divisional_charts.find((item) => item.division === divisionName);
  const groups = Array.from({ length: 12 }, () => []);
  division.planets.forEach((planet) => {
    const index = style === "north" ? planet.house - 1 : planet.sign;
    groups[index].push(`${glyphs[planet.planet]} ${planet.planet.slice(0, 2).toUpperCase()}`);
  });
  const ascSign = division.ascendant.sign;
  document.querySelector("#ascendant").textContent = `${signs[ascSign]} ${degrees(division.ascendant.degrees_in_sign)}`;
  const cells = groups.map((items, index) => {
    const cell = document.createElement("div");
    cell.className = `chart-cell cell-${index + 1}`;
    const label = style === "north" ? `H${index + 1}` : signs[index].slice(0, 3);
    const ascendantHere = style === "north" ? index === 0 : index === ascSign;
    cell.innerHTML = `<span>${label}${ascendantHere ? " · ASC" : ""}</span><strong>${items.join(" ") || "—"}</strong>`;
    return cell;
  });
  kundliChart.replaceChildren(...cells);
}

function renderDasha(dasha) {
  document.querySelector("#dasha-title").textContent = `${dasha.birth_lord} at birth`;
  document.querySelector("#dasha-balance").textContent = `${dasha.balance_years.toFixed(2)} years remaining`;
  const timeline = document.querySelector("#dasha-timeline");
  timeline.replaceChildren(...dasha.periods.map((period, index) => {
    const item = document.createElement("article");
    item.className = index === 0 ? "dasha-period active" : "dasha-period";
    const start = new Date(period.start).toISOString().slice(0, 10);
    const end = new Date(period.end).toISOString().slice(0, 10);
    item.innerHTML = `<span>${glyphs[period.lord]}</span><div><strong>${period.lord}</strong><small>${start} → ${end}</small></div><b>${period.duration_years}y</b>`;
    return item;
  }));
}

function renderRules(rules) {
  const list = document.querySelector("#rules-list");
  list.replaceChildren(...rules.map((rule) => {
    const item = document.createElement("article");
    item.className = `rule-result ${rule.present ? "present" : "absent"}`;
    item.innerHTML = `<span>${rule.present ? "✓" : "—"}</span><div><strong>${rule.name}</strong><small>${rule.evidence[0]}</small><em>${rule.source.title} · ${rule.source.section}</em></div><b>${rule.present ? "Matched" : "Not matched"}</b>`;
    item.title = rule.source.implemented_scope;
    return item;
  }));
}
