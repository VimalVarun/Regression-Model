import streamlit as st
import pandas as pd

from src.pipeline.predict_pipeline import PredictPipeline

# Load the trained model and scaler
predict_pipeline = PredictPipeline(model_path='artifacts/model.pkl', scaler_path='artifacts/scaler.pkl')

# Title of the app
st.title("Energy Production Prediction")

# User input for features
temperature = st.number_input("Temperature (°C)", min_value=-30.0, max_value=50.0, value=25.0)
exhaust_vacuum = st.number_input("Exhaust Vacuum (mmHg)", min_value=0.0, max_value=100.0, value=50.0)
amb_pressure = st.number_input("Ambient Pressure (kPa)", min_value=0.0, max_value=1033.300000, value=1009.100000)
r_humidity = st.number_input("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)

# Button to predict
if st.button("Predict Energy Production"):
    # Prepare input for prediction
    input_features = [temperature, exhaust_vacuum, amb_pressure, r_humidity]

    # Make prediction using the predict pipeline
    prediction = predict_pipeline.predict(input_features)

    # Display result
    st.success(f"Predicted Energy Production: {prediction:.2f}")