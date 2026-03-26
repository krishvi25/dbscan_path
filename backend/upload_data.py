import pandas as pd
from pymongo import MongoClient

# -----------------------------
# MongoDB Connection
# -----------------------------

MONGO_URI = "mongodb+srv://krishvi:krishvik@m0.fayormx.mongodb.net/?appName=M0"

client = MongoClient(MONGO_URI, tls=True)
db = client["mapDB"]
collection = db["Points"]

# -----------------------------
# Read Excel File
# -----------------------------
#df = pd.read_excel("2023-Panaji-Final.xlsx", header=1)
#df = pd.read_excel("2023-Mapusa-Final.xlsx", header=1) //done till here 



df = pd.read_excel("2023-Colvale-Final.xlsx", header=1)
#df = pd.read_excel("2023-Porvorim-Final.xlsx", header=1)
#df = pd.read_excel("2023-Anjuna-Final.xlsx", header=1)
#df = pd.read_excel("2024-Anjuna-Final.xlsx", header=1)
#df = pd.read_excel("2024-Colvale-Final.xlsx", header=1)
#df = pd.read_excel("2024-Mapusa-Final.xlsx", header=1)
#df = pd.read_excel("2024-Panaji-Final.xlsx", header=1)
#df = pd.read_excel("2024-Porvorim-Final.xlsx", header=1)

# -----------------------------
# Clean Column Names Properly
# -----------------------------
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.replace("\n", " ", regex=True)
    .str.replace("  ", " ", regex=True)
)

print("\n✅ Columns detected:")
for col in df.columns:
    print(repr(col))

# -----------------------------
# Remove Completely Empty Columns
# -----------------------------
df = df.dropna(axis=1, how="all")

# -----------------------------
# Standardize Latitude & Longitude Names
# -----------------------------
rename_map = {}
for col in df.columns:
    col_lower = col.lower()
    if "lat" in col_lower:
        rename_map[col] = "Latitude"
    if "lon" in col_lower or "long" in col_lower:
        rename_map[col] = "Longitude"
df.rename(columns=rename_map, inplace=True)

# -----------------------------
# Convert Date Column
# -----------------------------
if "Accident Date & Time" in df.columns:
    df["Accident Date & Time"] = pd.to_datetime(
        df["Accident Date & Time"],
        errors="coerce"
    )
    df = df[df["Accident Date & Time"].notna()]
    df["Accident Date & Time"] = df["Accident Date & Time"].dt.to_pydatetime()

# -----------------------------
# Convert Numeric Columns
# -----------------------------
numeric_columns = [
    "Vehicle Count", "Insured", "Uninsured", "Total",
    "Killed", "Grievous Injury", "Minor Injury",
    "No Injury", "Latitude", "Longitude", "Age"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Required Columns for Dashboard (Added Taluka & Area)
# -----------------------------
required_columns = [
    "Accident ID",
    "Accident Date & Time",
    "Accident Location",
    "Taluka",       # NEW
    "Area",         # NEW
    "Vehicle Count",
    "Severity",
    "Weather Condition",
    "Type of Accident",
    "Vehicle Type",
    "Insured",
    "Uninsured",
    "Total",
    "Killed",
    "Grievous Injury",
    "Minor Injury",
    "No Injury",
    "Latitude",
    "Longitude",
    "Cause",
    "Age"
]

existing_columns = [col for col in required_columns if col in df.columns]
df = df[existing_columns]

# -----------------------------
# Replace NaN with None (Mongo Safe)
# -----------------------------
df = df.where(pd.notnull(df), None)

# -----------------------------
# Debug: Check Lat/Lon Before Insert
# -----------------------------
if "Latitude" in df.columns and "Longitude" in df.columns:
    print("\n📍 Sample Latitude/Longitude values:")
    print(df[["Latitude", "Longitude"]].head())
else:
    print("\n❌ Latitude or Longitude column NOT found!")

# -----------------------------
# Convert to Dictionary
# -----------------------------
data = df.to_dict("records")
print("\n📊 Total records to insert:", len(data))

# -----------------------------
# Insert into MongoDB
# -----------------------------
if len(data) > 0:
    # collection.delete_many({})   # Uncomment if you want to clear old data
    collection.insert_many(data)
    print("\n✅ Dashboard-Ready Data Uploaded Successfully")
else:
    print("\n❌ No data to insert")