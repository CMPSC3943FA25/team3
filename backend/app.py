from flask import Flask, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

plant_data_path = os.path.join(
    os.path.dirname(__file__), 'data', 'plant_data.json')

# PUT /api/plant to create a plant


@app.put("/api/plant")
def create_plant():
    try:
        # Get create plant request json
        req = request.get_json()

        # Get "database" (current a file)
        with open(plant_data_path, "r") as file:
            plant_data = json.load(file)
            return '[]', 200

        # Append to database. Might add a filter later to overwrite with same name, but unnecessary for now
        plant_data.append(req)

        # Update database
        with open(plant_data_path, "w") as file:
            file.write(json.dumps(plant_data, indent=4))

        return "200 OK", 200
    except Exception as e:
        print(e)
        return "Internal Server Error", 200

# POST /api/search to search a plant


@app.post("/api/search")
def search_plants():
    try:
        # Get search json
        req = request.get_json()

        # Load "database" (currently a file)
        with open(plant_data_path, "r") as file:
            plant_data = json.load(file)

        if len(plant_data) == 0:
            print("No plant data loaded!")
            return '[]', 200

        # Now we start filtering based on request params
        if req["poisonous"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "poisonous") == req["poisonous"]]

        if req["difficulty"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "difficulty") == req["difficulty"]]

            # Filter by drought tolerance
        if req["drought_tolerant"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "drought_tolerant") == req["drought_tolerant"]]

        if req["water_frequency_min_hours"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "water_frequency_min_hours") == req["water_frequency_min_hours"]]

        if req["water_frequency_min_hours"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "water_frequency_max_hours") == req["water_frequency_max_hours"]]

        if req["repot_frequency_min_hours"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "repot_frequency_min_hours") == req["repot_frequency_min_hours"]]

        if req["repot_frequency_min_hours"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "repot_frequency_min_hours") == req["repot_frequency_min_hours"]]

        # Check if request soil is a subset of a plant's soil
        if req["soils"] is not None:
            plant_data = [p for p in plant_data if set(
                req.get("soils")).issubset(set(p.get("soils")))]

        if req["lighting"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "lighting") == req["lighting"]]

        if req["humidity"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "humidity") == req["humidity"]]

        # Fast growth filter
        if req["grow_speed"] is not None:
            if req["grow_speed"] == "fast":
                plant_data = [p for p in plant_data
                    if p.get("repot_frequency_min_months") <= 6]
            elif req["grow_speed"] == "slow":
                plant_data = [p for p in plant_data
                    if p.get("repot_frequency_min_months") > 6]

        if req["portability"] is not None:
            plant_data = [p for p in plant_data if p.get(
                "portability") == req["portability"]]

        if req["colors"] is not None:
            plant_data = [p for p in plant_data if set(
                req.get("colors")).issubset(set(p.get("colors")))]

        # Check if request seasons is a subset of a plant's seasons
        if req["seasons"] is not None:
            plant_data = [p for p in plant_data if set(
                req.get("seasons")).issubset(set(p.get("seasons")))]

        # Check if request hardiness is a subset of a plant's hardiness
        if req["hardiness"] is not None:
            plant_data = [p for p in plant_data if set(
                req.get("hardiness")).issubset(set(p.get("hardiness")))]

        if req["min_temperature"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "min_temperature") >= p.get("min_temperature")]

        if req["max_temperature"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "max_temperature") <= p.get("max_temperature")]

        if req["max_height"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "max_height") >= p.get("max_height_feet")]

        if req["max_spread"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "max_spread") >= p.get("max_spread_feet")]

        if req["min_expected_lifespan_years"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "min_expected_lifespan_years") <= p.get("min_expected_lifespan_years")]

        if req["max_expected_lifespan_years"] is not None:
            plant_data = [p for p in plant_data if req.get(
                "max_expected_lifespan_years") >= p.get("max_expected_lifespan_years")]

        # Return filtered (currently just returns request for testing)
        return json.dumps(plant_data, indent=4)
    except Exception as e:
        print(e)
        return "Internal Server Error", 500


if __name__ == "__main__":
    app.run(debug=True)
