# This file contains the routes for account-related tasks

# Import app info from app.py
from app import app
# For password hashing
import hashlib
# MySQL
import MySQLdb
# Import database connection from db.py
import db
# Flask
from flask import redirect, render_template, request, session, url_for, Blueprint
# RegEx (Prevent invalid input)
import re

# Define account blueprint
account = Blueprint('account', __name__)

# Password hashing function
def hashPassword(password):
    pwdBytes = password.encode()
    hash = hashlib.sha256(pwdBytes)
    return hash.hexdigest()

# Login page
@account.route('/', methods=['GET', 'POST'])
def login():
    # Error message (if any)
    error = ''

    # Get POST requests (username/password)
    if request.method == 'POST':

        # Get username and password from form
        username = request.form['username']
        password = hashPassword(request.form['password'])

        # Make sure there is text in the username and password boxes
        if (username is not None and password is not None):
            # MySQL (check for account)
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute MySQL query to check for account
            cursor.execute('SELECT * from accounts WHERE username = %s AND password = %s', (username, password))
            # Return record
            account = cursor.fetchone()
    
        # If cursor.fetchone() returns an account
        if account:
            # Set session data
            session['loggedIn'] = True
            session['username'] = account['username']
            # Redirect to Dashboard
            return redirect(url_for('dashboard.dash'))
        else:
            # Login failed
            error = 'Incorrect Credentials!'
    
    return render_template('index.html', error = error)

# Registration page
@account.route('/register', methods=['GET', 'POST'])
def register():
    # Error message (if any)
    error = ''

    # Get POST requests (username/password)
    if request.method == 'POST':

        # Get username and password from form
        username = request.form['username']
        password = hashPassword(request.form['password'])
        
        # Make sure there is text in the username and password boxes
        if (username is not None and password is not None):
            # MySQL (Check if account already exists)
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute MySQL query to check for account
            cursor.execute('SELECT * from accounts WHERE username = %s', (username,))
            # Return record
            account = cursor.fetchone()
    
        # If cursor.fetchone() returns an account
        if account:
            error = "An account already exists with this username."
        # Check if desired username is valid
        elif not re.match('[a-zA-z\-_0-9]', username):
            error = "Username must only contain letters, numbers, dashes, and underscores."
        # Create account
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s)', (username, password))
            db.mysql.connection.commit()
            error = "Registration Successful!"

    return render_template('register.html', error = error)

# Logout
@account.route('/logout')
def logout():
    # Pop session data
    session.pop('loggedIn', None)
    session.pop('username', None)

    # Redirect to login
    return redirect(url_for('account.login'))