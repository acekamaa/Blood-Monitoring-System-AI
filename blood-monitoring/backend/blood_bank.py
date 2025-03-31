from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BloodBank(db.Model):
    __tablename__ = 'blood_bank'
    bloodbank_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    blood_quantity = db.Column(db.Integer, nullable=False)  # Stored in pints
    blood_bank_county = db.Column(db.String(100), nullable=False)
    blood_bank_name = db.Column(db.String(100), nullable=False)

def check_blood_levels():
    # Check blood stock levels and return an alert if levels are low.
    
    blood_levels = BloodBank.query.all()
    low_stock_threshold = 50  # Minimum pints of blood required

    results = []
    for record in blood_levels:
        status = "Sufficient"
        if record.quantity < low_stock_threshold:
            status = "Low Stock - Replenish Needed"
        
        results.append({
            "blood_type": record.blood_type,
            "blood_quantity": record.blood_quantity,
            "blood_bank_county": record.blood_bank_county,
            "blood_bank_name": record.blood_bank_name,
            "status": status
        })

    return results
