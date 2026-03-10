import mongoose from "mongoose";

const pointSchema = new mongoose.Schema({
  Latitude: Number,
  Longitude: Number
}, { 
  strict: false,
  collection: "Points"
});


const Points = mongoose.model("Points", pointSchema);
export default Points;