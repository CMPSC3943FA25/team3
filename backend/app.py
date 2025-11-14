from flask import Flask, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)

# ✅ CORS configuration (must come after app is created)
CORS(app, resources={r"/*": {
    "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
    "allow_headers": "*",
    "methods": ["GET", "POST", "OPTIONS"]
}})


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods",
                         "GET,PUT,POST,DELETE,OPTIONS")
    return response


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
     "allow_headers": "*", "methods": ["GET", "POST", "OPTIONS"]}})

plant_data_path = os.path.join(os.path.dirname(__file__), 'data', 'plant_data.json')

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
feature/nerish-branch
        if "poisonous" in req and req["poisonous"] != "any":
            plant_data = [p for p in plant_data if p.get(
                "poisonous") == req["poisonous"]]

        if len(plant_data) == 0:
            print("No plant data after Poisonous")
            return '[]', 200

        if "difficulty" in req and req["difficulty"] != "any":
            plant_data = [p for p in plant_data if p.get(
                "difficulty") == req["difficulty"]]

            # Filter by maintenance level
        if "maintenance" in req and req["maintenance"] != "any":
            plant_data = [p for p in plant_data if p.get(
                "maintenance") == req["maintenance"]]

        if len(plant_data) == 0:
            print("No plant data after Maintenance Level")
            return '[]', 200

        if len(plant_data) == 0:
            print("No plant data after Difficulty")
            return '[]', 200

        if "water_every_n_hours" in req:
            water_frequency = req.get("water_frequency")
            plant_data = [
                p for p in plant_data if (
                    # If the user wants to water plants once per week, we need to filter for plants between the earliest and latest
                    (water_frequency >= p.get("water_every_n_hours").get("start"))
                    and
                    (water_frequency <= p.get("water_every_n_hours").get("end"))
                )
            ]

        if len(plant_data) == 0:
            print("No plant data after Water Frequency")
            return '[]', 200

        if "repot_frequency" in req:
            report_frequency = req.get("repot_frequency")
            plant_data = [
                p for p in plant_data if (
                    (repot_frequency >= p.get("repot_every_n_months").get("start"))
                    and
                    (repot_frequency <= p.get("repot_every_n_months").get("end"))
                )
            ]

        if len(plant_data) == 0:
            print("No plant data after Repot Frequency")
            return '[]', 200

        # Check if request soil is a subset of a plant's soil
        if "soil" in req:
            plant_data = [p for p in plant_data if set(
                req.get("soil")).issubset(set(p.get("soil")))]

        if len(plant_data) == 0:
            print("No plant data after Soil")
            return '[]', 200

        if "lighting" in req and req["lighting"] != "any":
            plant_data = [p for p in plant_data if p.get(
                "lighting") == req["lighting"]]

        if len(plant_data) == 0:
            print("No plant data after Lighting")
            return '[]', 200

        if "humidity" in req and req["humidity"] != "any":
            plant_data = [p for p in plant_data if p.get(
                "humidity") == req["humidity"]]

        if len(plant_data) == 0:
            print("No plant data after Humidity")
            return '[]', 200

        # Check if request seasons is a subset of a plant's seasons
        print(set(req.get("seasons")))
        if "seasons" in req:
            plant_data = [p for p in plant_data if set(
                req.get("seasons")).issubset(set(p.get("seasons")))]

        if len(plant_data) == 0:
            print("No plant data after Seasons")
            return '[]', 200

        # Check if request hardiness is a subset of a plant's hardiness
        if "hardiness" in req:
            plant_data = [p for p in plant_data if set(
                req.get("hardiness")).issubset(set(p.get("hardiness")))]

        if len(plant_data) == 0:
            print("No plant data after Hardiness")
            return '[]', 200

        if "min_temp" in req:
            plant_data = [p for p in plant_data if req.get(
                "min_temp") >= p.get("temperature").get("min")]

        if len(plant_data) == 0:
            print("No plant data after Min Temp")
            return '[]', 200

        if "max_temp" in req:
            plant_data = [p for p in plant_data if req.get(
                "max_temp") <= p.get("temperature").get("max")]

        if len(plant_data) == 0:
            print("No plant data after Max Temp")
            return '[]', 200
        # Return filtered (currently just returns request for testing)
        return json.dumps(plant_data, indent=4)
    except Exception as e:
        print(e)
        return "Internal Server Error", 500


print("Starting Flask server...")

if __name__ == "__main__":
    app.run(debug=True)
