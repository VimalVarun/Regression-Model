import streamlit as st
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

# Instantiate the prediction pipeline
predict_pipeline = PredictPipeline()

# Streamlit App
st.title('Energy Production Prediction App')

# Input sliders for each independent feature
temperature = st.slider('Temperature (°C)', min_value=10.0, max_value=100.0, step=0.1)
exhaust_vacuum = st.slider('Exhaust Vacuum (cm Hg)', min_value=20.0, max_value=100.0, step=0.1)
amb_pressure = st.slider('Ambient Pressure (mm Hg)', min_value=50.0, max_value=1033.0, step=0.1)
r_humidity = st.slider('Relative Humidity (%)', min_value=20.0, max_value=100.0, step=0.1)

# When the button is clicked, predict the energy production
if st.button('Predict Energy Production'):
    try:
        # Prepare input data as a DataFrame
        input_data = pd.DataFrame({
            'temperature': [temperature],
            'exhaust_vacuum': [exhaust_vacuum],
            'amb_pressure': [amb_pressure],
            'r_humidity': [r_humidity]
        })

        # Use the PredictPipeline to make predictions
        prediction = predict_pipeline.predict(input_data)[0]
        
        # Display the prediction
        st.success(f'The predicted energy production is: {prediction:.2f} MW')

    except Exception as e:
        st.error(f"Error during prediction: {e}")