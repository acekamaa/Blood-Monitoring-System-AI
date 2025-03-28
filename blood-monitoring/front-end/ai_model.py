# ai_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Simulated data (replace with real data)
data = {
    'blood_type': ['A+', 'O-', 'B+', 'A+', 'O-'],
    'county': ['Nairobi', 'Kisumu', 'Mombasa', 'Nairobi', 'Kisumu'],
    'demand': [10, 5, 8, 12, 4],  # Historical demand
    'shortage': [0, 1, 0, 1, 1]   # 1 = shortage, 0 = no shortage
}
df = pd.DataFrame(data)

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

# Save model
joblib.dump(model, 'blood_shortage_model.pkl')
joblib.dump(le_blood, 'le_blood.pkl')
joblib.dump(le_county, 'le_county.pkl')

# Prediction function
def predict_shortage(blood_type, county, demand):
    model = joblib.load('blood_shortage_model.pkl')
    le_blood = joblib.load('le_blood.pkl')
    le_county = joblib.load('le_county.pkl')
    input_data = [[le_blood.transform([blood_type])[0], le_county.transform([county])[0], demand]]
    return model.predict(input_data)[0]

# Example
print(predict_shortage('A+', 'Nairobi', 15))  # 1 = shortage, 0 = no shortage