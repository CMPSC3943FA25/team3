let CURRENT_RESULTS = [];
async function Search() {
  let poisonous = document.querySelector("#poisonous").value;
  if (poisonous === "true") poisonous = true;
  else if (poisonous === "false") poisonous = false;
  else poisonous = "any";

  const search = {
    poisonous: poisonous,
    difficulty: document.querySelector("#difficulty").value,
    lighting: document.querySelector("#lighting").value,
    humidity: document.querySelector("#humidity").value,
    temperature: {
      min: Number(document.querySelector("#min_temp").value),
      max: Number(document.querySelector("#min_temp").value),
    },
    soil: Array.from(document.querySelectorAll(".soil"))
      .filter((x) => x.checked)
      .map((x) => x.value),
    seasons: Array.from(document.querySelectorAll(".season"))
      .filter((x) => x.checked)
      .map((x) => x.value),
  };
  // console.log(search);
  const res = await fetch("http://127.0.0.1:5000/api/search", {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify(search),
  });
  const json = await res.json();
  PopulateResults(json);
}

// Makes names pretty. e.g. deciduous_soil -> Deciduous Soil
function NormalizeName(str) {
  return str
    .split("_")
    .map((x) => x[0].toUpperCase() + x.slice(1))
    .join(" ");
}

function PopulateResults(plants) {
  CURRENT_RESULTS = Array.isArray(plants) ? plants : [];
  const plant_list = document.querySelector("#plant_list");
  plant_list.innerHTML = "";

  console.log(plants);

  for (const plant of plants) {
    const panel = document.createElement("div");
    panel.className = "plant";

    const name = document.createElement("h2");
    name.textContent = NormalizeName(plant.name);
    panel.appendChild(name);

    const difficulty = document.createElement("p");
    difficulty.textContent = "Difficulty: " + NormalizeName(plant.difficulty);
    panel.appendChild(difficulty);

    const water_frequency = document.createElement("p");
    if (
      plant.water_every_n_hours.start % 24 === 0 &&
      plant.water_every_n_hours.end % 24 === 0
    )
      water_frequency.textContent =
        "Water every " +
        plant.water_every_n_hours.start / 24 +
        " to " +
        plant.water_every_n_hours.end / 24 +
        " days";
    else {
      water_frequency.textContent =
        "Water every " +
        plant.water_every_n_hours.start +
        " to " +
        plant.water_every_n_hours.end +
        " hours";
    }
    panel.appendChild(water_frequency);

    const soils = document.createElement("p");
    soils.textContent = `Soils: ${plant.soil
      .map((x) => NormalizeName(x))
      .join(", ")}`;
    panel.appendChild(soils);

    const lighting = document.createElement("p");
    lighting.textContent = `Lighting: ${NormalizeName(plant.lighting)}`;
    panel.appendChild(lighting);

    const humidity = document.createElement("p");
    humidity.textContent = `Humidity: ${NormalizeName(plant.humidity)}`;
    panel.appendChild(humidity);

    const seasons = document.createElement("p");
    seasons.textContent = `Seasons: ${plant.seasons
      .map((x) => NormalizeName(x))
      .join(", ")}`;
    panel.appendChild(seasons);

    // TODO: If it is continious such as 1a, 1b, 2a, 2b, 3a, make it disply 1a-3a
    const hardiness = document.createElement("p");
    hardiness.textContent = `Hardiness Zones: ${plant.hardiness
      .map((x) => NormalizeName(x))
      .join(", ")}`;
    panel.appendChild(hardiness);

    const temperature = document.createElement("p");
    temperature.textContent = `Temperature: ${plant.temperature.min}-${plant.temperature.max}`;
    panel.appendChild(temperature);

    const poisonous = document.createElement("p");
    poisonous.textContent = plant.poisonous
      ? "Plant is Poisonous"
      : "Plant is not Poisonous";
    panel.appendChild(poisonous);

    plant_list.appendChild(panel);
  }
}
// ===============================
// EXPORT FEATURE – CLIENT-SIDE
// ===============================

// Flatten nested objects/arrays into dot-path keys for CSV
function flatten(obj, prefix = "", out = {}) {
  if (obj === null || obj === undefined) return out;
  if (Array.isArray(obj)) {
    out[prefix.slice(0, -1)] = obj.join(", ");
    return out;
  }
  if (typeof obj !== "object") {
    out[prefix.slice(0, -1)] = obj;
    return out;
  }
  for (const [k, v] of Object.entries(obj)) {
    flatten(v, `${prefix}${k}.`, out);
  }
  return out;
}

// Convert an array of objects to CSV text
function toCSV(rows) {
  if (!rows || rows.length === 0) return "";
  const flatRows = rows.map(r => flatten(r));
  const headers = Array.from(
    flatRows.reduce((set, r) => {
      Object.keys(r).forEach(k => set.add(k));
      return set;
    }, new Set())
  );
  const esc = (val) => {
    if (val === null || val === undefined) return "";
    const s = String(val);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const lines = [
    headers.join(","),
    ...flatRows.map(r => headers.map(h => esc(r[h])).join(","))
  ];
  return lines.join("\n");
}

// Trigger a download
function downloadFile(filename, mime, text) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function exportJSON() {
  if (!CURRENT_RESULTS.length) {
    alert("No results to export.");
    return;
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const pretty = JSON.stringify(CURRENT_RESULTS, null, 2);
  downloadFile(`growsmart-results-${stamp}.json`, "application/json", pretty);
}

function exportCSV() {
  if (!CURRENT_RESULTS.length) {
    alert("No results to export.");
    return;
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  // UTF-8 BOM improves Excel compatibility
  const csv = "\uFEFF" + toCSV(CURRENT_RESULTS);
  downloadFile(`growsmart-results-${stamp}.csv`, "text/csv;charset=utf-8", csv);
}

// Wire buttons when DOM is ready
window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("exportCsvBtn")?.addEventListener("click", exportCSV);
  document.getElementById("exportJsonBtn")?.addEventListener("click", exportJSON);
});
