# ai_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# Simulated data (replace with real data)
data = {
    'blood_type': ['A+', 'O-', 'B+', 'A+', 'O-'],
    'county': ['Nairobi', 'Kisumu', 'Mombasa', 'Nairobi', 'Kisumu'],
    'demand': [10, 5, 8, 12, 4],  # Historical demand
    'shortage': [0, 1, 0, 1, 1]   # 1 = shortage, 0 = no shortage
}
df = pd.DataFrame(data)

# Create category mappings BEFORE converting to numbers
blood_type_mapping = {b: i for i, b in enumerate(df['blood_type'].astype('category').cat.categories)}
county_mapping = {c: i for i, c in enumerate(df['county'].astype('category').cat.categories)}

# Convert categorical columns to numeric
df['blood_type'] = df['blood_type'].map(blood_type_mapping)
df['county'] = df['county'].map(county_mapping)

# Preprocess
le_blood = LabelEncoder()
le_county = LabelEncoder()
df['blood_type'] = le_blood.fit_transform(df['blood_type'])
df['county'] = le_county.fit_transform(df['county'])

# Train model
X = df[['blood_type', 'county', 'demand']]
y = df['shortage']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# make predictions
y_pred = model.predict(X_test)

# evaluate model accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, 'blood_shortage_model.pkl')
joblib.dump(le_blood, 'le_blood.pkl')
joblib.dump(le_county, 'le_county.pkl')

# Prediction function
def predict_shortage(blood_type, county, demand):
    # model = joblib.load('blood_shortage_model.pkl')
    # le_blood = joblib.load('le_blood.pkl')
    # le_county = joblib.load('le_county.pkl')
    # input_data = [[le_blood.transform([blood_type])[0], le_county.transform([county])[0], demand]]
    # return model.predict(input_data)[0]
    if blood_type not in blood_type_mapping or county not in county_mapping:
        return "Invalid Blood Type or County"
    
    blood_type_code = blood_type_mapping[blood_type]
    county_code = county_mapping[county]
    input_data = pd.DataFrame([[blood_type_code, county_code, demand]], columns=['blood_type', 'county', 'demand'])

    prediction = model.predict(input_data)[0]
    return "Shortage Expected" if prediction == 1 else "No Shortage"

# Example
print(predict_shortage('A+', 'Nairobi', 15))  # 1 = shortage, 0 = no shortage