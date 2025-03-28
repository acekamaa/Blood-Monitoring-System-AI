import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os
import joblib
import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define models
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(),
    "Logistic Regression": LogisticRegression(max_iter=200)
}

# Load preprocessed data
df = pd.read_csv("C:/Users/kev/Desktop/blood-monitoring/backend/dummydata/preprocessed_data.csv")
print("Data loaded successfully.")

# Features and target variable
X = df.drop(columns=["Person ID", "Blood Type"])  # Features
y = df["Blood Type"]  # Target variable

#training set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)  # Train model
    y_pred = model.predict(X_test)  # Predict on test set
    acc = accuracy_score(y_test, y_pred)  # Calculate accuracy
    print(f"{name} Accuracy: {acc:.2f}")
    print(classification_report(y_test, y_pred))
