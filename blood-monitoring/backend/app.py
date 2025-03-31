from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
from dotenv import load_dotenv
from flask_cors import CORS
import os
from datetime import datetime
from ai_model import predict_shortage  # Updated import
from blood_bank import check_blood_levels

# Load environment variables
load_dotenv()
print("Environment variables loaded")

# PostgreSQL connection details
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST') 
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Check if environment variables are set
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Database connection details are not fully set in environment variables.")

# Print the database connection details for debugging
print(f"Connecting to database {DB_NAME} at {DB_HOST}:{DB_PORT} with user {DB_USER}")

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
print("CORS enabled for all routes")

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print("SQLAlchemy configured with the database URI")
print("\U0001F517 Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

# Enable debugging mode
app.config['DEBUG'] = True
print("Debugging mode enabled")

# Set up the database connection
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 1800,
}
print("SQLAlchemy engine options set")

# Initialize SQLAlchemy
db = SQLAlchemy(app)
print("SQLAlchemy initialized")
# Check if the database connection is successful
app.app_context().push()
print("App context pushed")
try:
    db.engine.connect()
    print("Database connection successful")
except Exception as e:
    print(f"Error connecting to the database: {e}")

# Define the BloodRecord model
class BloodRecord(db.Model):
    __tablename__ = 'blood_record'
    bloodbank_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    print("BloodRecord model defined")

    def __repr__(self):
        return f"<BloodRecord {self.blood_type} - {self.county} - {self.date}>"

# Create the database table if it doesn't exist
with app.app_context():
    db.create_all()
    print("Database tables created")

# Submit API
@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    if not all(k in data for k in ('bloodType', 'county', 'date', 'demand')):
        return jsonify({'message': 'Missing fields'}), 400
    
    record = BloodRecord(
        blood_type=data['bloodType'],
        county=data['county'],
        date=data['date'],
        demand=data['demand']
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Data submitted successfully'})

# Update API
@app.route('/api/update/<int:id>', methods=['PUT'])
def update_data(id):
    data = request.get_json()
    record = BloodRecord.query.get(id)
    if not record:
        return jsonify({'message': 'Record not found'}), 404
    
    record.blood_type = data.get('bloodType', record.blood_type)
    record.county = data.get('county', record.county)
    record.date = data.get('date', record.date)
    record.demand = data.get('demand', record.demand)
    db.session.commit()
    return jsonify({'message': 'Record updated successfully'})

# Delete API
@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    record = BloodRecord.query.get(id)
    if not record:
        return jsonify({'message': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# health check for docker
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200

# API to predict blood shortages
@app.route('/api/predict-shortage', methods=['POST'])
def shortage_prediction():
    """
    API to predict blood shortage based on input data.
    Expected JSON input: {"blood_type": "A+", "county": "Nairobi", "demand": 15}
    """
    data = request.get_json()
    
    # Validate input
    if "blood_type" not in data or "county" not in data or "demand" not in data:
        return jsonify({"error": "Missing parameters"}), 400

    # Get input values
    blood_type = data["blood_type"]
    county = data["county"]
    demand = data["demand"]

    # Make prediction
    prediction_result = predict_shortage(blood_type, county, demand)

    return jsonify({"prediction": prediction_result})

# Check blood level
@app.route('/api/check-blood-level', methods=['GET'])
def get_blood_levels():
    """
    API to check blood levels in blood banks.
    Returns a list of all blood types with their stock status.
    """
    data = check_blood_levels()
    
    if not data:
        return jsonify({"message": "No blood records found"}), 404
    
    return jsonify({"blood_levels": data})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
