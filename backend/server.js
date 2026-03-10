import express from "express";
import mongoose from "mongoose";
import fetch from "node-fetch";
import cors from "cors";
import Points from "./model/Points.js";
const app = express();

app.use(cors());
app.use(express.json());

/* ---------------- MongoDB connection ---------------- */

mongoose.connect("mongodb://127.0.0.1:27017/mapDB");

mongoose.connection.on("connected", () => {
  console.log("MongoDB connected");
});

mongoose.connection.on("error", (err) => {
  console.log("MongoDB error:", err);
});

/* ---------------- MongoDB model ---------------- */

const pointSchema = new mongoose.Schema({
  Latitude: Number,
  Longitude: Number
});


/* ---------------- Get Points ---------------- */

app.get("/Points", async (req, res) => {
  try {
    const points = await Points.find({});
    console.log("Fetched:", points.length);
    res.json(points);
  } catch (err) {
    console.log(err);
    res.status(500).json({ error: err.message });
  }
});

/* ---------------- Search API ---------------- */

app.get("/search", async (req, res) => {
  const q = req.query.q;

  if (!q) return res.json([]);

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}&limit=5`,
      {
        headers: {
          "User-Agent": "smart-navigator-app"
        }
      }
    );

    const data = await response.json();
    res.json(data);

  } catch (err) {
    res.status(500).json({ error: "Search failed" });
  }
});

/* ---------------- Start server ---------------- */

const PORT = 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});