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
        with open("plant_data.json", "r") as file:
            plant_data = json.load(file)

        # Append to database. Might add a filter later to overwrite with same name, but unnecessary for now
        plant_data.append(req)

        # Update database
        with open("plant_data.json", "w") as file:
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
        
        # TODO: Now we start filtering based on request params

        # Return filtered (currently just returns request for testing)
        return json.dumps(req, indent=4)
    except Exception as e:
        print(e)
        return "Internal Server Error", 500
