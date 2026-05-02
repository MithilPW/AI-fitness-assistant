"""
Machine Learning Model for Calorie Prediction
Uses scikit-learn RandomForestRegressor to predict daily calorie needs
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class CaloriePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = ['age', 'height', 'weight', 'gender', 'activity_level']

    def train(self, df):
        """
        Train the calorie prediction model

        Args:
            df: DataFrame with features and 'daily_calories' column
        """
        X = df[self.feature_names]
        y = df['daily_calories']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Model trained successfully!")
        print(f"MSE: {mse:.2f}")
        print(f"R² Score: {r2:.4f}")
        print(f"Feature Importance:\n{self._get_feature_importance()}")

        return self

    def predict(self, age, height, weight, gender, activity_level):
        """
        Predict daily calorie requirement

        Args:
            age: User age
            height: User height (cm)
            weight: User weight (kg)
            gender: 0 for Female, 1 for Male
            activity_level: Activity multiplier (1-1.9)

        Returns:
            Predicted daily calories (float)
        """
        if self.model is None:
            raise ValueError("Model not trained yet!")

        X = np.array([[age, height, weight, gender, activity_level]])
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]

        return max(1200, prediction)  # Minimum 1200 calories for safety

    def _get_feature_importance(self):
        """Get feature importance from the model"""
        importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
        return sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    def save(self, filepath):
        """Save model and scaler"""
        with open(filepath, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
        print(f"Model saved to {filepath}")

    def load(self, filepath):
        """Load model and scaler"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
        print(f"Model loaded from {filepath}")
        return self

def train_and_save_model():
    """Main function to train and save model"""
    # Load dataset
    df = pd.read_csv('data/fitness_dataset.csv')

    # Create and train predictor
    predictor = CaloriePredictor()
    predictor.train(df)

    # Save model
    os.makedirs('models', exist_ok=True)
    predictor.save('models/calorie_predictor.pkl')

    return predictor

if __name__ == '__main__':
    train_and_save_model()
