from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration details
    app.config['COSMOS_DB_URI'] = os.getenv("COSMOS_DB_URI")
    app.config['COSMOS_DB_KEY'] = os.getenv("COSMOS_DB_KEY")
    app.config['DATABASE_NAME'] = os.getenv("DATABASE_NAME")
    app.config['CONVERSATION_LOG_CONTAINER'] = os.getenv("CONVERSATION_LOG_CONTAINER")
    app.config['CONVERSATION_ERROR_CONTAINER'] = os.getenv("CONVERSATION_ERROR_CONTAINER")

    with app.app_context():
        # Register blueprints or routes
        from . import routes
        app.register_blueprint(routes.bp)

    return app
