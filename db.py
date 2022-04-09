# This file handles the MySQL connection

# MySQL Connector
from flask_mysqldb import MySQL
# Get variables from config.py
import config

mysql = MySQL()