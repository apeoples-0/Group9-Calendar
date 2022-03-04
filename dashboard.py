# This file contains the routes for dashboard related tasks

from app import app
from flask import Flask, session, render_template, redirect, url_for

# Dashboard
@app.route('/dashboard')
def dashboard():

    # Check if user is logged in
    if 'loggedIn' in session:
        # Go to Dashboard
        return render_template('dashboard.html', username=session['username'])
    
    # If user is not logged in, redirect to /login
    return redirect(url_for('login'))