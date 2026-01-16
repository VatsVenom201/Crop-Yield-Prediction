import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.title("Crop Yield Prediction")

model = joblib.load("model.pkl")

st.header("Enter Soil and Weather Details")

# numeric parser with validation tracking

invalid_numeric_fields = []
missing_numeric_fields = []

def parse_numeric(value, field_name):
    if value.strip() == "":
        missing_numeric_fields.append(field_name)
        return np.nan
    try:
        return float(value)
    except ValueError:
        invalid_numeric_fields.append(field_name)
        return np.nan

N = parse_numeric(st.text_input("Nitrogen (N)"), "Nitrogen")
P = parse_numeric(st.text_input("Phosphorus (P)"), "Phosphorus")
K = parse_numeric(st.text_input("Potassium (K)"), "Potassium")

Soil_pH = parse_numeric(st.text_input("Soil pH"), "Soil pH")
Soil_Moisture = parse_numeric(st.text_input("Soil Moisture (%)"), "Soil Moisture")

Organic_Carbon = parse_numeric(st.text_input("Organic Carbon (0-1)"), "Organic Carbon")

Temperature = parse_numeric(st.text_input("Temperature (°C)"), "Temperature")
Humidity = parse_numeric(st.text_input("Humidity (%)"), "Humidity")
Rainfall = parse_numeric(st.text_input("Rainfall (mm)"), "Rainfall")
Sunlight_Hours = parse_numeric(st.text_input("Sunlight Hours"), "Sunlight Hours")
Wind_Speed = parse_numeric(st.text_input("Wind Speed (km/h)"), "Wind Speed")

Altitude = parse_numeric(st.text_input("Altitude (meters)"), "Altitude")
Fertilizer_Used = parse_numeric(st.text_input("Fertilizer Used (kg/ha)"), "Fertilizer Used")
Pesticide_Used = parse_numeric(st.text_input("Pesticide Used (kg/ha)"), "Pesticide Used")

# Categorical handling + missing tracking
missing_categorical_fields = []

def parse_category(value, field_name):
    if value == "Unknown":
        missing_categorical_fields.append(field_name)
        return np.nan
    return value
Soil_Type = parse_category(
    st.selectbox("Soil Type", ["Clay", "Sandy", "Silt", "Loamy"]),
    "Soil Type"
)

Region = parse_category(
    st.selectbox("Region", ["South", "East", "North", "West", "Central"]),
    "Region"
)

Season = parse_category(
    st.selectbox("Season", ["Rabi", "Kharif", "Zaid"]),
    "Season"
)

Crop_Type = parse_category(
    st.selectbox("Crop Type", ["Rice", "Wheat", "Potato", "Cotton", "Maize", "Sugarcane"]),
    "Crop Type"
)

Irrigation_Type = parse_category(
    st.selectbox("Irrigation Type", ["Drip", "Canal", "Rainfed", "Sprinkler"]),
    "Irrigation Type"
)
# making dataframe of input to pass it to model

input_df = pd.DataFrame([{
    "N": N,
    "P": P,
    "K": K,
    "Soil_pH": Soil_pH,
    "Soil_Moisture": Soil_Moisture,
    "Soil_Type": Soil_Type,
    "Organic_Carbon": Organic_Carbon,
    "Temperature": Temperature,
    "Humidity": Humidity,
    "Rainfall": Rainfall,
    "Sunlight_Hours": Sunlight_Hours,
    "Wind_Speed": Wind_Speed,
    "Region": Region,
    "Altitude": Altitude,
    "Season": Season,
    "Crop_Type": Crop_Type,
    "Irrigation_Type": Irrigation_Type,
    "Fertilizer_Used": Fertilizer_Used,
    "Pesticide_Used": Pesticide_Used
}])

if invalid_numeric_fields:
    st.error(
        "Invalid numeric input detected in: "
        + ", ".join(invalid_numeric_fields)
    )

if missing_numeric_fields or missing_categorical_fields:
    st.warning(
        "Some fields were left empty and will be auto-filled by the model:\n"
        + ", ".join(missing_numeric_fields + missing_categorical_fields)
    )

if st.button("Predict Crop Yield"):

    if invalid_numeric_fields:
        st.stop()  # Block prediction if invalid inputs exist

    prediction = model.predict(input_df)

    st.success(f"Predicted Crop Yield: {prediction[0]:.2f} tons/hectare")

    # Show which values were imputed
    if missing_numeric_fields or missing_categorical_fields:
        st.info(
            "The following fields were missing and were auto-imputed:\n"
            + ", ".join(missing_numeric_fields + missing_categorical_fields)
        )
