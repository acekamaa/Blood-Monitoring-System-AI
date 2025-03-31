from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the database
db = SQLAlchemy()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Enable CORS
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register Blueprints (routes)
    from .routes import main
    app.register_blueprint(main)

    # Create database tables if not exist
    with app.app_context():
        db.create_all()

    return app
