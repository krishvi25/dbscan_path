const express = require("express");
const fetch = require("node-fetch");
const cors = require("cors");

const app = express();
app.use(cors());

app.get("/search", async (req, res) => {
  const q = req.query.q;

  if (!q) return res.json([]);

  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        q
      )}&limit=5`,
      {
        headers: {
          "User-Agent": "smart-navigator-app",
        },
      }
    );

    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: "Search failed" });
  }
});

app.listen(5000, () =>
  console.log("Server running on port 5000")
);