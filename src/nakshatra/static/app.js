const form = document.querySelector("#birth-form");
const emptyState = document.querySelector("#empty-state");
const results = document.querySelector("#results");
const errorBox = document.querySelector("#error");
const planetGrid = document.querySelector("#planet-grid");
const submitButton = form.querySelector("button[type='submit']");
const kundliChart = document.querySelector("#kundli-chart");
const chartTabs = document.querySelectorAll(".chart-tab");
let currentChart = null;

const signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
const glyphs = { sun: "☉", moon: "☾", mercury: "☿", venus: "♀", mars: "♂", jupiter: "♃", saturn: "♄", rahu: "☊", ketu: "☋" };

const degrees = (value) => `${value.toFixed(4)}°`;

chartTabs.forEach((tab) => tab.addEventListener("click", () => {
  chartTabs.forEach((item) => item.classList.toggle("active", item === tab));
  kundliChart.className = `kundli-chart ${tab.dataset.chart}`;
  if (currentChart) renderKundli(currentChart, tab.dataset.chart);
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
  document.querySelector("#ascendant").textContent = `${signs[chart.houses.ascendant.sign]} ${degrees(chart.houses.ascendant.degrees_in_sign)}`;
  renderKundli(chart, document.querySelector(".chart-tab.active").dataset.chart);
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
  const groups = Array.from({ length: 12 }, () => []);
  chart.planets.forEach((planet) => {
    const index = style === "north" ? planet.house - 1 : planet.sign.sign;
    groups[index].push(`${glyphs[planet.planet]} ${planet.planet.slice(0, 2).toUpperCase()}`);
  });
  const ascSign = chart.houses.ascendant.sign;
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
