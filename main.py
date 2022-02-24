# Used for hashing passwords
import hashlib
# MySQL library
import MySQLdb
# Flask framework
from flask import Flask, redirect, render_template, request, session, url_for
# Flask MySQL connector
from flask_mysqldb import MySQL
# RegEx (Prevent invalid input)
import re

app = Flask(__name__)

# Secret Key (Needed for sessions in Flask)
app.secret_key = 'A secret key.'

# MySQL database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'webcalendar'

mysql = MySQL(app)

# Password hashing function
def hashPassword(password):
    pwdBytes = password.encode()
    hash = hashlib.sha256(pwdBytes)
    return hash.hexdigest()

# Login page
@app.route('/', methods=['GET', 'POST'])
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            error = 'Incorrect Credentials!'
    
    return render_template('index.html', error = error)

# Logout
@app.route('/logout')
def logout():
    # Pop session data
    session.pop('loggedIn', None)
    session.pop('username', None)

    # Redirect to login
    return redirect(url_for('login'))



# Registration page
@app.route('/register', methods=['GET', 'POST'])
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
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
            mysql.connection.commit()
            error = "Registration Successful!"

    return render_template('register.html', error = error)

# Dashboard
@app.route('/dashboard')
def dashboard():

    # Check if user is logged in
    if 'loggedIn' in session:
        # Go to Dashboard
        return render_template('dashboard.html', username=session['username'])
    
    # If user is not logged in, redirect to /login
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run()