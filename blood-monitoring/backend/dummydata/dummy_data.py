import pandas as pd
import random

# Define distributions based on general estimates
blood_types = {
    "O+": 37, "O-": 6, "A+": 27, "A-": 4,
    "B+": 23, "B-": 2, "AB+": 2, "AB-": 1
}

# Normalize probabilities
blood_type_choices = list(blood_types.keys())
blood_type_probs = [v / sum(blood_types.values()) for v in blood_types.values()]

# Kenyan counties for location simulation
kenyan_counties = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
    "Thika", "Nyeri", "Meru", "Machakos", "Garissa"
]

def generate_dummy_data(num_samples=10000):
    data = []
    for i in range(num_samples):
        person_id = f"P{i+1:04d}"
        age = random.randint(18, 65)
        gender = random.choice(["Male", "Female"])
        blood_type = random.choices(blood_type_choices, weights=blood_type_probs, k=1)[0]
        location = random.choice(kenyan_counties)
        donated_last_year = random.choice([True, False])

        data.append([person_id, age, gender, blood_type, location, donated_last_year])

    df = pd.DataFrame(data, columns=["Person ID", "Age", "Gender", "Blood Type", "Location", "Donated Last Year"])
    return df

# Generate data and save to CSV
df = generate_dummy_data(10000)
df.to_csv("blood_type_dummy_data.csv", index=False)

print("Dummy data generated and saved as 'blood_type_dummy_data.csv'")