import streamlit as st
from src.pipeline.predict_pipeline import PredictPipeline

# Load the trained model and scaler
try:
    predict_pipeline = PredictPipeline(model_path='artifacts/model.pkl', scaler_path='artifacts/scaler.pkl')
except Exception as e:
    st.error(f"Error loading model or scaler: {e}")

# Title of the app
st.title("Energy Production Prediction")

# User input for features with correct numeric types
temperature = st.number_input("Temperature (°C)", min_value=-30.0, max_value=50.0, value=25.0)
exhaust_vacuum = st.number_input("Exhaust Vacuum (mmHg)", min_value=0.0, max_value=100.0, value=50.0)
amb_pressure = st.number_input("Ambient Pressure (kPa)", min_value=0.0, max_value=1033.3, value=1009.1)
r_humidity = st.number_input("Relative Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)

# Button to predict
if st.button("Predict Energy Production"):
    try:
        # Prepare input for prediction
        input_features = [temperature, exhaust_vacuum, amb_pressure, r_humidity]

        # Make prediction using the predict pipeline
        prediction = predict_pipeline.predict(input_features)

        # Display result
        st.success(f"Predicted Energy Production: {prediction:.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")