from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import requests

app = Flask(__name__)
CORS(app)  # allow React frontend requests

# ---------------- MongoDB Connection ----------------
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

if MONGO_URI:
    client = MongoClient(MONGO_URI)  # Render
else:
    client = MongoClient("mongodb+srv://krishvi:krishvik@m0.fayormx.mongodb.net/mapDB")  # Local

db = client["mapDB"]
points_collection = db["Points"]
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
        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": q,
            "format": "json",
            "limit": 5
        }

        headers = {
            "User-Agent": "KrishviNavigatorApp/1.0 (krishvi@email.com)"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        # 👇 DEBUG THIS
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text[:200])

        if response.status_code != 200:
            return jsonify([])

        return jsonify(response.json())

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify([])

# ---------------- Run Server ----------------
@app.route("/")
def home():
    return {"message": "API running"}
# ---------------- Run Server ----------------
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))  # Render provides PORT

    app.run(host="0.0.0.0", port=port, debug=False)