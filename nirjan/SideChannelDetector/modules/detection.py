from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

class AnomalyDetector:
    def __init__(self, model_path="data/models/iso_forest.pkl"):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False
        self.model_path = model_path

    def train(self, training_data):
        """
        Train the model on 'clean' data.
        training_data: numpy array of shape (n_samples, n_features)
        """
        print("Training Anomaly Detector on initial data stream...")
        self.model.fit(training_data)
        self.is_trained = True
        # joblib.dump(self.model, self.model_path) # Optional persistence

    def predict(self, scaled_features):
        """
        Predict if the current sample is anomalous.
        Returns: -1 for outlier, 1 for inlier
        """
        if not self.is_trained:
            return 1 # Assume normal if not trained
        
        return self.model.predict(scaled_features)[0]

    def decision_function(self, scaled_features):
        if not self.is_trained:
            return 0
        return self.model.decision_function(scaled_features)[0]
