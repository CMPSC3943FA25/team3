function submitForm(event) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);

  let water_start = Number(formData.get("water_start"));
  let water_end = Number(formData.get("water_end"));

  if (formData.get("period") === "days") {
    water_start *= 24;
    water_end *= 24;
  }

  const json = {
    [formData.get("name")]: {
      poisonous: formData.get("poisonous") !== null,
      difficulty: formData.get("difficulty"),
      water_every_n_hours: {
        start: water_start,
        end: water_end,
      },
      repot_every_n_months: {
        start: Number(formData.get("repot_start")),
        end: Number(formData.get("repot_end")),
      },
      soil: Array.from(form.querySelectorAll('input[name="soil"]:checked')).map(
        (x) => x.value
      ),
      lighting: formData.get("lighting"),
      humidity: formData.get("humidity"),
      seasons: Array.from(
        form.querySelectorAll('input[name="seasons"]:checked')
      ).map((x) => x.value),
      hardiness: Array.from(
        form.querySelectorAll('input[name="hardiness"]:checked')
      ).map((x) => x.value),
      temperature: {
        min: Number(formData.get("min_temperature")),
        max: Number(formData.get("max_temperature")),
      },
    },
  };

  console.log(json);

  fetch("http://127.0.0.1:5000/api/plant", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(json),
  });
}
