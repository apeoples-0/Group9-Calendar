# Flask framework
from flask import Flask
# Import Flask app info
from app import app
# Import account blueprint
from account import account
# Import dashboard blueprint
from dashboard import dashboard

# Register the needed blueprints
app.register_blueprint(account)
app.register_blueprint(dashboard)

if __name__ == '__main__':
   app.run()