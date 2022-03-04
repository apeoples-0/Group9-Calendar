# This file handles the MySQL connection

# Import app from app.py
from app import app
# MySQL Connector
from flask_mysqldb import MySQL
# Get variables from config.py
import config

# MySQL database connection
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)