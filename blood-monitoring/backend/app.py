from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date
from dotenv import load_dotenv
from flask_cors import CORS
import os
from datetime import datetime
from dummydata.blood_prediction import predict_shortage
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
print("🔗 Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

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
    __tablename__ = 'blood_records'
    bloodbank_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    blood_bank_county = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    print("BloodRecord model defined")

    def __repr__(self):
        return f"<BloodRecord {self.blood_type} - {self.blood_bank_county} - {self.date}>"
    
print(BloodRecord.__repr__(BloodRecord))

# Create the database table if it doesn't exist
with app.app_context():
    db.create_all()
    print("Database tables created")

# health check for docker
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200

# api to predict blood shortages
@app.route('/api/predict-shortage', methods=['POST'])
def shortage_prediction():
    """
    API to predict blood shortage based on input data.
    Expected JSON input: {"blood_stock": 100, "blood_demand": 120}
    """
    data = request.get_json()

    # Validate input
    if "blood_stock" not in data or "blood_demand" not in data:
        return jsonify({"error": "Missing parameters"}), 400

    # Get input values
    blood_stock = data["blood_stock"]
    blood_demand = data["blood_demand"]

    # Make prediction
    prediction_result = predict_shortage(blood_stock, blood_demand)

    return jsonify({"prediction": prediction_result})

# check blood level
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

# API route to submit data 'http:127.0.0.1.5000/api/submit'
print("Setting up API route to submit data")
@app.route('/api/submit', methods=['POST'])
def submit_data():
    print("Received request to submit data")
    data = request.get_json()
        
    # Debugging: Print the received data
    print("Received data:", data)
        
    # Validate required fields
    if not all(k in data for k in ('bloodType', 'county', 'date')):
       return jsonify({'message': 'Missing fields'}), 400
        
    # Convert date string to date object
    formatted_date = datetime.strptime(data['date'], "%Y-%m-%d").date()

    try:
        # Create a new BloodRecord instance
        record = BloodRecord(
            blood_type=data['bloodType'], 
            county=data['county'], 
            date=formatted_date
        )

        # Add the record to the session and commit
        db.session.add(record)
        db.session.commit()
    
        return jsonify({'message': 'Data submitted successfully'}), 201
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error submitting data: {e}")
        return jsonify({'error': str(e)}), 500
    
# API route to get data 
@app.route('/api/get_data', methods=['GET'])
def get_data():
    print("Received request to get data")
    try:
        # Query all records from the database
        records = BloodRecord.query.all()
        
        # Convert records to a list of dictionaries
        data = [{'id': record.id, 'blood_type': record.blood_type, 'county': record.county, 'date': record.date.isoformat()} for record in records]
        
        return jsonify(data), 200
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error retrieving data: {e}")
        return jsonify({'error': str(e)}), 500
    
# API route to delete data
@app.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    print(f"Received request to delete data with id: {id}")
    print(f"Checking record ID: {id}")

    try:
        # Query the record by ID
        record = BloodRecord.query.get(id)
        
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        # Delete the record from the session and commit
        db.session.delete(record)
        db.session.commit()
        
        return jsonify({'message': 'Record deleted successfully'}), 200
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error deleting data: {e}")
        return jsonify({'error': str(e)}), 500
    
# API route to update data
@app.route('/api/update/<int:id>', methods=['PUT'])
def update_data(id):
    print(f"Received request to update data with id: {id}")
    try:
        data = request.get_json()
        
        # Debugging: Print the received data
        print("Received data:", data)
        
        # Query the record by ID
        record = BloodRecord.query.get(id)

        # Validate required fields
        if not all(k in data for k in ('bloodType', 'county', 'date')):
            return jsonify({'message': 'Missing fields'}), 400
         
        if not record:
            return jsonify({'message': 'Record not found'}), 404
        
        # Update the record
        record.blood_type = data['bloodType']
        record.county = data['county']
        record.date = datetime.strptime(data['date'], "%Y-%m-%d").date()
        
        # Commit the changes
        db.session.commit()
        
        return jsonify({'message': 'Record updated successfully'}), 200
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error updating data: {e}")
        return jsonify({'error': str(e)}), 500
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
