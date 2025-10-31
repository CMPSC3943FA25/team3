from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.put("/api/plant")
def create_plant():
    try:
        req = request.get_json()
        with open("plant_data.json", "r") as file:
            plant_data = json.load(file)
        plant_data[next(iter(req))] = next(iter(req.values()))
        with open("plant_data.json", "w") as file:
            file.write(json.dumps(plant_data, indent=4))
        return "200 OK", 200
    except:
        return "Internal Server Error", 200

@app.post("/api/search")
def search_plants():
    try:
        req = request.get_json()
        with open("plant_data.json", "r") as file:
            plant_data = json.load(file)
        print(plant_data)
        return json.dumps(req, indent=4)
    except:
        return "Internal Server Error", 500