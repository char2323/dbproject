from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# Create extension instances
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# If an unauthenticated user tries to access a protected page,
# flask_login will flash a message and redirect. We don't need a redirect
# URL here since our admin panel handles it, but we set up the manager.
login_manager.login_view = 'api.Session_login' # This is still useful for some contexts

def create_app():
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, origins="http://localhost:5173", supports_credentials=True)

    # Import and register blueprints
    from .api import api_bp as api_blueprint
    app.register_blueprint(api_blueprint)
    
    # Import and initialize Flask-Admin
    from .admin import admin
    admin.init_app(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    """
    Required callback for Flask-Login. Loads a user from the database given a user_id.
    """
    from .models import User
    # Use db.session.get for primary key lookups
    return db.session.get(User, int(user_id))
