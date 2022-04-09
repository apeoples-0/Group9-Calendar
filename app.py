# This file handles the Flask application

# Import config information
import config
from flask import Flask

# Import account blueprint
from account import account
# Import dashboard blueprint
from dashboard import dashboard

# Import MySQL connection
from db import mysql

# Define Flask app
app = Flask(__name__)

# Secret Key (Needed for sessions in Flask)
app.secret_key = config.SECRET_KEY

# Flask session time
app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME

# Register the needed blueprints
app.register_blueprint(account)
app.register_blueprint(dashboard)

# MySQL database connection
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql.init_app(app)