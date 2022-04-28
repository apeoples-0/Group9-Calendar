# This file contains the routes for dashboard related tasks

from multiprocessing import Event, shared_memory
from tracemalloc import start
import MySQLdb
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
             "rrule" : event['ruleString'],
             "enddate" : event['endTime'],
             "id" : event['eventID'],
             "color" : event['color'],
             #TODO: PROPERLY IMPLEMENT ALLDAY EVENTS
             "allDay" : 'false'
        })

    return events

# Load holidays
def loadHolidays():
    # Get holidays query
    getHolidaysQuery = '''
            SELECT *
            FROM holidays
    '''
    cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(getHolidaysQuery)

    # Store the holidays from the database in eventsSQL
    holidaysSQL = cursor.fetchall()
    
    # Create holidays array for frontend
    holidays = []

    # Add holidays
    for event in holidaysSQL:
        holidays.append({
             "name" : event['eventName'],
             "startdate" : event['startTime'],
             "enddate" : event['endTime'],
             "id" : 'None',
             "color" : event['color'],
             "allDay" : 'true'
        })

    return holidays

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

    return(convertedDate)

# Dashboard
@dashboard.route('/dashboard')
def dash():

    # Check if user is logged in
    if 'loggedIn' in session:
        # Add events and holidays (if requested) to the calendar
        events = []
        
        # Add calendar events
        for event in loadEvents():
            events.append(event)

        # If holidays are enabled, add them as well
        if 'holidays' in session and session['holidays'] == 1:
            for event in loadHolidays():
                events.append(event)

        # Go to Dashboard
        return render_template('calendar.html', events = events)
    
    # If user is not logged in, redirect to /login
    return redirect(url_for('account.login'))

@dashboard.route('/addevent', methods=['GET', 'POST'])
def addEvent():
    # Get form data
    eventName = request.form['eventName']
    startDateTime = request.form['startDateTime']
    endDateTime = request.form['endDateTime']
    color = getCSSColor(request.form['eventColor'])
    rulestring = ruleToString()

    if 'allDay' in request.form:
        allDay = 1
    else:
        allday = 0

    if request.method == 'POST':
        if 'loggedIn' in session:
            if ((eventName == "" or None)):
                return render_template('addeventfailed.html')
            if ((eventName != "" or None) and (startDateTime != "" or None)):
                cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO events VALUES (NULL, %s, %s, %s, 0, %s, %s)', (eventName, rulestring, convertDateTime(startDateTime),
                convertDateTime(endDateTime), session['userID'], allDay, color ))
                db.mysql.connection.commit()
    return redirect(url_for('dashboard.dash'))

@dashboard.route('/sharedevent', methods=['GET', 'POST'])
def sharedEvent():
    # Get event ID from URL
    eventID = request.args.get("e")

    # Get information about shared event
    getEventQuery = ''' 
            SELECT *
            FROM events
            WHERE eventID = %s AND shareable = 1
            '''
    cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(getEventQuery, eventID)

    # Store the received event
    event = cursor.fetchone()

    if event == None:
        return render_template('eventnotfound.html')
    else:
        return render_template('sharedEvent.html', event = event)

@dashboard.route('/addsharedevent', methods=['GET', 'POST'])
def addSharedEvent():
    if request.method == 'POST':
        if 'loggedIn' in session:
            # Get event to add
            getEventQuery = ''' 
            SELECT *
            FROM events
            WHERE eventID = %s
            '''
            cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(getEventQuery, request.form['eventID'])

            # Store the received event
            event = cursor.fetchone()

            # Insert the event into the user's calendar
            cursor.execute('INSERT INTO events VALUES (NULL, %s, %s, %s, %s, 1, %s)', (event['eventName'], event['startTime'],
                event['endTime'], session['userID'], event['color'])) 
            db.mysql.connection.commit()  

            return redirect(url_for('dashboard.dash'))
        else:
            # If the user does not have an account, inform them that one is needed.
            return render_template('notloggedin.html')



@dashboard.route('/modifyevent', methods=['GET', 'POST'])
def modifyEvent():
    if request.method == 'POST':
        if 'loggedIn' in session:
            if "delete" in request.form:
                # If the event being modified is a holiday, return an error
                if request.form['delete'] == 'None':
                    return render_template('holidayerror.html')

                cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('DELETE FROM events WHERE eventID=%s AND userID=%s', (request.form['delete'], session['userID']))
                db.mysql.connection.commit()
                return redirect(url_for('dashboard.dash'))
            if "share" in request.form:
                # If the event being modified is a holiday, return an error
                if request.form['share'] == 'None':
                    return render_template('holidayerror.html')

                # Make event shareable
                cursor = db.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('''
                UPDATE events
                SET
                    shareable = 1
                WHERE
                    eventID = %s
                ''', (request.form['share']))
                db.mysql.connection.commit()

                # Redirect to shared page
                return redirect(url_for('dashboard.sharedEvent') + '?e=' + request.form['share'])

    return redirect(url_for('dashboard.dash'))

# Gets the CSS color (more visually appealing) based on the name provided
def getCSSColor(color):
    match color:
        case "Blue":
            return "royalblue"
        case "Red":
            return "firebrick"
        case "Orange":
            return "orange"
        case "Yellow":
            return "gold"
        case "Green":
            return "darkgreen"
        case "Purple":
            return "purple"

#Get and Convert rule info into a string
""""
def ruleToString():
rule = new RRule({
  freq: getFreq(request.form['recurrtype']),
  count: request.form['countnum'],
})
ruleString = rule.tostring()
return ruleString
"""
#Gets the frequency from the addeventmodal
def getFreq(freq):
    match freq:
        case "Daily":
            return "RRule.DAILY"
        case "Weekly":
            return "RRule.WEEKLY"
        case "Monthly":
            return "RRule.MONTHLY"
        case "Yearly":
            return "RRule.YEARLY"