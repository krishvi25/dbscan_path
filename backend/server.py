from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import requests

app = Flask(__name__)
CORS(app)  # allow React frontend requests

# ---------------- MongoDB Connection ----------------
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["mapDB"]
points_collection = db["Points"]

print("MongoDB connected")

# ---------------- Get Points ----------------
@app.route("/Points", methods=["GET"])
def get_points():

    points_cursor = points_collection.find({}, {"_id": 0})

    valid_points = []

    for p in points_cursor:
        lat = p.get("Latitude")
        lng = p.get("Longitude")

        # skip invalid values
        if lat is None or lng is None:
            continue

        try:
            lat = float(lat)
            lng = float(lng)
        except:
            continue

        # skip NaN
        if str(lat) == "nan" or str(lng) == "nan":
            continue

        valid_points.append({
            "Latitude": lat,
            "Longitude": lng
        })

    print("Valid points:", len(valid_points))

    return jsonify(valid_points)
# ---------------- Search API ----------------
@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    if not q:
        return jsonify([])

    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={q}&limit=5"
        headers = {"User-Agent": "smart-navigator-app"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        print("Search failed:", e)
        return jsonify({"error": "Search failed"}), 500

# ---------------- Run Server ----------------
# ---------------- Run Server ----------------
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))  # Render provides PORT

    app.run(host="0.0.0.0", port=port, debug=False)