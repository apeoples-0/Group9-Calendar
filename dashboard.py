# This file contains the routes for dashboard related tasks

from app import app
from flask import session, render_template, redirect, url_for, Blueprint

# Define dashboard blueprint
dashboard = Blueprint('dashboard', __name__)

# Dashboard
@dashboard.route('/dashboard')
def dash():

    # Check if user is logged in
    if 'loggedIn' in session:
        # Go to Dashboard
        return render_template('calendar.html')
    
    # If user is not logged in, redirect to /login
    return redirect(url_for('account.login'))

@dashboard.route('/addevent')
def addEvent():
    return render_template("addeventmodal.html")