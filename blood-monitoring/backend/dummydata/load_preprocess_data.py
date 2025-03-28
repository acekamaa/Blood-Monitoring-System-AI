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

# Load dummy data
print(os.getcwd())
df = pd.read_csv("C:/Users/kev/Desktop/blood-monitoring/backend/dummydata/blood_type_dummy_data.csv")
print("Data loaded successfully.")  

# Encode categorical features (Gender, Location, Donated Last Year)
encoder = LabelEncoder()
df["Gender"] = encoder.fit_transform(df["Gender"])  # Male=1, Female=0
df["Location"] = encoder.fit_transform(df["Location"])
df["Donated Last Year"] = df["Donated Last Year"].astype(int)  # True=1, False=0

# Encode Blood Type (Target Variable)
df["Blood Type"] = encoder.fit_transform(df["Blood Type"])

# Features and target variable
X = df.drop(columns=["Person ID", "Blood Type"])  # Features
y = df["Blood Type"]  # Target variable

# Split dataset into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features (optional, but can help with some classifiers)
X_train = (X_train - X_train.mean()) / X_train.std()
X_test = (X_test - X_train.mean()) / X_train.std()  # Use training mean/std for normalization

# Initialize classifiers
classifiers = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "SVC": SVC(random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=200, random_state=42)
}

# Train and evaluate each classifier
for name, clf in classifiers.items():
    # Train the classifier
    clf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = clf.predict(X_test)
    
    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=encoder.inverse_transform([0, 1, 2, 3, 4, 5, 6, 7]))
    
    print(f"Classifier: {name}")
    print(f"Accuracy: {accuracy:.2f}")
    print(report)

# Save the trained models (optional, for later use)
import joblib
import os

# Create a directory to save models if it doesn't exist
if not os.path.exists("models"):
    os.makedirs("models")

for name, clf in classifiers.items():
    joblib.dump(clf, f"models/{name.replace(' ', '_').lower()}.joblib")
print("Models saved to 'models/' directory.")

# Save the encoder for later use
joblib.dump(encoder, "models/label_encoder.joblib")
print("Label encoder saved to 'models/' directory.")

# Save the preprocessed data for later use
# df.to_csv("backend/dummydata/preprocessed_data.csv", index=False)
df.to_csv("C:/Users/kev/Desktop/blood-monitoring/backend/dummydata/preprocessed_data.csv", index=False)
print("Preprocessed data saved as 'preprocessed_data.csv'.")
