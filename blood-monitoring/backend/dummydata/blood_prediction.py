import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

def train_model():
    # Train a basic machine learning model for predicting blood shortages.
    # Sample training dataset (historical blood supply & demand)
    data = {
        "blood_stock": [100, 200, 50, 30, 500, 600, 40, 20, 90, 250],
        "blood_demand": [120, 180, 60, 40, 490, 580, 50, 30, 100, 230],
        "shortage": [1, 0, 1, 1, 0, 0, 1, 1, 1, 0]  # 1 = shortage, 0 = no shortage
    }
    
    df = pd.DataFrame(data)

    # Features (X) and target variable (y)
    X = df[["blood_stock", "blood_demand"]]
    y = df["shortage"]

    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train a simple model
    model = LogisticRegression()
    model.fit(X_scaled, y)

    # Save model and scaler
    joblib.dump(model, "shortage_model.pkl")
    joblib.dump(scaler, "scaler.pkl")

def predict_shortage(blood_stock, blood_demand):
    """
    Predict blood shortage based on current stock and demand.
    """
    # Load model and scaler
    model = joblib.load("shortage_model.pkl")
    scaler = joblib.load("scaler.pkl")

    # Prepare input data
    X_new = scaler.transform([[blood_stock, blood_demand]])

    # Make prediction
    prediction = model.predict(X_new)[0]
    return "Shortage Expected" if prediction == 1 else "Sufficient Stock"

# Train model initially
if __name__ == "__main__":
    train_model()
