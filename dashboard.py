# This file contains the routes for dashboard related tasks

from tracemalloc import start
import MySQLdb
from app import app
from flask import request, session, render_template, redirect, url_for, Blueprint
# Import database connection from db.py
import db
# For splitting time string
import re

# Define dashboard blueprint
dashboard = Blueprint('dashboard', __name__)

# Load Events
def loadEvents():
    # Get logged in user's events from database
    getEventsQuery = ''' 
            SELECT *
            FROM events
            WHERE userID = %s
            '''
    cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(getEventsQuery, str(session['userID']))

    # Store the events from the database in eventsSQL
    eventsSQL = cursor.fetchall()

    # Create events array to be passed to the frontend
    events = []

    # Add events
    for event in eventsSQL:
        events.append({
             "name" : event['eventName'],
             "startdate" : event['startTime'],
             "enddate" : event['endTime']
        })

    return events

# Convert datetimepicker string to date object
def convertDateTime(date):
    # Split date into month, day, year, hour, minute, AM/PM
    dateList = re.split('\s|,|\/|:',date)

    # Convert hour to 24 hour time
    if dateList[5] == "PM":
        dateList[3] = str(int(dateList[3]) + 12)

    # Concatenate the string in the way MySQL expects
    convertedDate = '-'.join([dateList[2],dateList[0],dateList[1]])
    convertedDate = ' '.join([convertedDate, dateList[3]])
    convertedDate = ':'.join([convertedDate, dateList[4], "00"])
    
    print(convertedDate)

    return(convertedDate)

# Dashboard
@dashboard.route('/dashboard')
def dash():

    # Check if user is logged in
    if 'loggedIn' in session:
        # Go to Dashboard
        return render_template('calendar.html', events = loadEvents())
    
    # If user is not logged in, redirect to /login
    return redirect(url_for('account.login'))

@dashboard.route('/addevent', methods=['GET', 'POST'])
def addEvent():
    # Get form data
    eventName = request.form['eventName']
    startDateTime = request.form['startDateTime']
    endDateTime = request.form['endDateTime']

    if request.method == 'POST':
        if ((eventName == "" or None)):
            return render_template('addeventfailed.html')
        if ((eventName != "" or None) and (startDateTime != "" or None)):
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO events VALUES (NULL, %s, %s, %s, %s)', (eventName, convertDateTime(startDateTime),
             convertDateTime(endDateTime), session['userID']))
            db.mysql.connection.commit()
    return redirect(url_for('dashboard.dash'))