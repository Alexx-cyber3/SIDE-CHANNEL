import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False
        # Buffer to hold history for statistical analysis (rolling window)
        self.history = collections.deque(maxlen=20) 
        self.window_size = 10

    def fit(self, initial_data):
        """
        Fit the scaler on initial calibration data using statistical features.
        """
        features_list = []
        temp_history = collections.deque(maxlen=self.window_size)
        
        for d in initial_data:
            raw = [d['power_proxy'], d['exec_time_proxy'], d['memory_proxy']]
            temp_history.append(raw)
            if len(temp_history) == self.window_size:
                features_list.append(self._extract_stats(list(temp_history)))
        
        if not features_list: # Fallback if data too short
            features_list = [[d['power_proxy'], d['exec_time_proxy'], d['memory_proxy'], 0, 0, 0] for d in initial_data]

        self.scaler.fit(features_list)
        self.is_fitted = True

    def _extract_stats(self, window):
        """Statistical Analysis: Extract mean and std dev from the signal window."""
        arr = np.array(window)
        means = np.mean(arr, axis=0)
        stds = np.std(arr, axis=0)
        # Combined feature vector: [raw_means..., raw_stds...]
        return np.concatenate([means, stds])

    def process(self, data_point):
        """
        Process a single data point using the statistical window.
        """
        raw = [data_point['power_proxy'], data_point['exec_time_proxy'], data_point['memory_proxy']]
        self.history.append(raw)
        
        if len(self.history) < self.window_size:
            # Not enough data for stats yet, return dummy/padded
            features = np.array([raw + [0, 0, 0]])
        else:
            window = list(self.history)[-self.window_size:]
            features = np.array([self._extract_stats(window)])
        
        if self.is_fitted:
            return self.scaler.transform(features)
        return features

import collections
