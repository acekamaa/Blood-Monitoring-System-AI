# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/blood_db'
db = SQLAlchemy(app)

class BloodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    if not all(k in data for k in ('bloodType', 'county', 'date')):
        return jsonify({'message': 'Missing fields'}), 400
    
    record = BloodRecord(blood_type=data['bloodType'], county=data['county'], date=data['date'])
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Data submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

# Add to app.py
@app.route('/api/blood-types', methods=['GET'])
def get_blood_types():
    result = db.session.query(BloodRecord.blood_type, db.func.count(BloodRecord.id).label('count'))\
                      .group_by(BloodRecord.blood_type).all()
    return jsonify([{'blood_type': r[0], 'count': r[1]} for r in result])