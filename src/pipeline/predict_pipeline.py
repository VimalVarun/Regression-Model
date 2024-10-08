import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

class PredictPipeline:
    def __init__(self, model_path, scaler_path=None):
        # Load the model and scaler if provided
        self.model = joblib.load(model_path)
        if scaler_path:
            self.scaler = joblib.load(scaler_path)
        else:
            self.scaler = None

    def predict(self, features):
        # Convert the features to a DataFrame if necessary
        if isinstance(features, list):
            features = np.array(features).reshape(1, -1)

        # If a scaler is used, apply scaling to the input features
        if self.scaler:
            features = self.scaler.transform(features)

        # Make a prediction
        prediction = self.model.predict(features)
        return prediction[0]