# This file handles the Flask application

# Import config information
import config
from flask import Flask

# Define Flask app
app = Flask(__name__)

# Secret Key (Needed for sessions in Flask)
app.secret_key = config.SECRET_KEY

# Flask session time
app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME