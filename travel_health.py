import json
from flask import Blueprint, request, jsonify

travel_health_bp = Blueprint('travel_health', __name__)

# ✅ Fix: Encoding issue solved here
with open("travel_data.json", "r", encoding="utf-8") as f:
    travel_data = json.load(f)

@travel_health_bp.route("/api/travel-health", methods=["POST"])
def travel_health_mode():
    data = request.get_json()
    destination = data.get("destination", "").lower()

    # Default checklist in case destination data is incomplete
    default_checklist = ["Carry first-aid kit", "Keep hand sanitizer and mask", "Stay hydrated"]
    
    # Check if destination exists in travel data
    city_data = travel_data.get(destination, None)

    if not city_data:
        return jsonify({"error": "Destination not found"}), 404  # Return a 404 error if the destination doesn't exist
    
    checklist = city_data.get("checklist", default_checklist)
    outbreaks = city_data.get("outbreaks", [])
    weather_risks = city_data.get("weather_risks", [])
    hospitals = city_data.get("hospitals", [])

    return jsonify({
        "checklist": checklist,
        "outbreaks": outbreaks,
        "weather_risks": weather_risks,
        "hospitals": hospitals
    })
