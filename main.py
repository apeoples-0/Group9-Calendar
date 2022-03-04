# Flask framework
from flask import Flask
# Import Flask app info
from app import app
# Import routes from account.py
from account import *
# Import routes from dashboard.py
from dashboard import *

if __name__ == '__main__':
   app.run()