# This file contains the routes for account-related tasks

# For password hashing
import hashlib
from turtle import update
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

    # Check if user is already logged in
    if 'loggedIn' in session:
        # Go to Dashboard
        return redirect(url_for('dashboard.dash'))

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
            session['userID'] = account['userID']
            session['holidays'] = int.from_bytes(account['holidays'], "big")
            session.permanent = True
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

        # Get username, password and backup passphrase from form
        username = request.form['username']
        password = hashPassword(request.form['password'])
        backupPhrase = hashPassword(request.form['backup'])
        
        # Make sure there is text in the username and password boxes
        if (username is not None and password is not None and backupPhrase is not None):
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
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, 1)', (username, password, backupPhrase))
            db.mysql.connection.commit()
            error = "Registration Successful!"

    return render_template('register.html', error = error)

# Account Management
@account.route('/management')
def management():
    # Error (if any)
    error = ''

    # Redirect to login
    return render_template('management.html', error = error, username=session['username'])

# Password Reset
@account.route('/passwordreset', methods=['GET', 'POST'])
def passwordReset():
    # Message (Error or Success)
    message = ''

    # Get POST requests (username/backup phrase/password)
    if request.method == 'POST':

         # Get username, new password and backup passphrase from form
        username = request.form['username']
        password = hashPassword(request.form['password'])
        backupPhrase = hashPassword(request.form['backup'])

        # Make sure there is text in the username, backup phrase, and password boxes
        if (username is not None and password is not None and backupPhrase is not None):
            # MySQL (check for account)
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute MySQL query to check for account
            cursor.execute('SELECT * from accounts WHERE username = %s AND backupphrase = %s', (username, backupPhrase))
            # Return record
            account = cursor.fetchone()

        # If cursor.fetchone() returns an account
        if account:
            updateQuery = ''' 
            UPDATE accounts
            SET password = %s
            WHERE username = %s
            '''
            cursor.execute(updateQuery, (password, username))
            db.mysql.connection.commit()
            message = "Password reset successful!"
        else:
            # Reset failed
            message = 'Username or backup phrase incorrect!'

    return render_template('passwordreset.html', message = message)

# Change Password
@account.route('/changepassword', methods=['GET', 'POST'])
def changePassword():
    # Message (Error or Success)
    message = ''

    # Get POST requests (old password/new password)
    if request.method == 'POST':

         # Get username, new password and backup passphrase from form
        oldPassword = hashPassword(request.form['old'])
        newPassword = hashPassword(request.form['new'])

        # Make sure there is text in both boxes
        if (oldPassword is not None and newPassword is not None):
            # MySQL (check for account)
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Execute MySQL query to check for account
            cursor.execute('SELECT * from accounts WHERE username = %s AND password = %s', (session['username'], oldPassword))
            # Return record
            account = cursor.fetchone()

        # If cursor.fetchone() returns an account
        if account:
            updateQuery = ''' 
            UPDATE accounts
            SET password = %s
            WHERE username = %s
            '''
            cursor.execute(updateQuery, (newPassword, session['username']))
            db.mysql.connection.commit()
            message = "Password change successful!"
        else:
            # Change failed
            message = 'Current password is incorrect!'

    return render_template('changepassword.html', message = message)

# Logout
@account.route('/logout')
def logout():
    # Pop session data
    session.pop('loggedIn', None)
    session.pop('username', None)
    session.pop('userID', None)
    session.pop('holidays', None)

    # Redirect to login
    return redirect(url_for('account.login'))

# Enable Holidays
@account.route('/enableholidays')
def enableHolidays():
    # MySQL cursor
    cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    updateQuery = ''' 
            UPDATE accounts
            SET holidays = 1
            WHERE username = %s
            '''

    # Enable holidays for the currently logged in user
    cursor.execute(updateQuery, (session['username'],))

    # Commit changes
    db.mysql.connection.commit()

    session['holidays'] = 1

    return redirect(url_for('account.management'))

# Disable Holidays
@account.route('/disableholidays')
def disableHolidays():
    # MySQL cursor
    cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    updateQuery = ''' 
            UPDATE accounts
            SET holidays = 0
            WHERE username = %s
            '''

    # Disable holidays for the currently logged in user
    cursor.execute(updateQuery, (session['username'],))

    # Commit changes
    db.mysql.connection.commit()

    session['holidays'] = 0

    return redirect(url_for('account.management'))