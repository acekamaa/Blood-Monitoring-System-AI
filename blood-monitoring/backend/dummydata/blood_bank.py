from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BloodBank(db.Model):
    __tablename__ = 'blood_bank'
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # Stored in pints
    location = db.Column(db.String(100), nullable=False)

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
            "quantity": record.quantity,
            "location": record.location,
            "status": status
        })

    return results
