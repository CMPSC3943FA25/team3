from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# PUT /api/plant to create a plant
@app.put("/api/plant")
def create_plant():
    try:
        # Get create plant request json
        req = request.get_json()

        # Get "database" (current a file)
        with open("./data/plant_data.json", "r") as file:
            plant_data = json.load(file)

        # Append to database. Might add a filter later to overwrite with same name, but unnecessary for now
        plant_data.append(req)

        # Update database
        with open("./data/plant_data.json", "w") as file:
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
        with open("plant_data.json", "r") as file:
            plant_data = json.load(file)
        
        # Now we start filtering based on request params
        if "poisonous" in req:
            plant_data = [p for p in plant_data if p.get("poisonous") == req["poisonous"]]

        if "difficulty" in req:
            plant_data = [p for p in plant_data if p.get("difficulty") == req["difficulty"]]

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
        
        if "repot_frequency" in req:
            report_frequency = req.get("repot_frequency")
            plant_data = [
                p for p in plant_data if (
                    (repot_frequency >= p.get("repot_every_n_months").get("start"))
                    and
                    (repot_frequency <= p.get("repot_every_n_months").get("end"))
                )
            ]

        # Check if request soil is a subset of a plant's soil
        if "soil" in req:
            plant_data = [p for p in plant_data if set(req.get("soil")).issubset(set(p.get("soil")))]

        if "lighting" in req:
            plant_data = [p for p in plant_data if p.get("lighting") == req["lighting"]]

        if "humidity" in req:
            plant_data = [p for p in plant_data if p.get("humidity") == req["humidity"]]

        # Check if request seasons is a subset of a plant's seasons
        if "seasons" in req:
            plant_data = [p for p in plant_data if set(req.get("seasons")).issubset(set(p.get("seasons")))]

        # Check if request hardiness is a subset of a plant's hardiness
        if "hardiness" in req:
            plant_data = [p for p in plant_data if set(req.get("hardiness")).issubset(set(p.get("hardiness")))]

        if "min_temp" in req:
            plant_data = [p for p in plant_data if req.get("min_temp") >= p.get("temperature").get("min")]
        
        if "max_temp" in req:
            plant_data = [p for p in plant_data if req.get("max_temp") <= p.get("temperature").get("max")]
            

        # Return filtered (currently just returns request for testing)
        return json.dumps(plant_data, indent=4)
    except Exception as e:
        print(e)
        return "Internal Server Error", 500
