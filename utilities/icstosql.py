# Generates the SQL statements to add the contents of an iCalendar file to SQL database

from ics import Calendar

# Configuration
tableName = 'holidays'
fileName = "holidays.ics"
color = 'black'

file = open(fileName, "r")

calendar = Calendar(file.read())

# The necessary sql statements will be printed to the terminal
for event in calendar.events:
    print("INSERT INTO {} VALUES (NULL, '{}', '{}', '{}', '{}');".format(tableName, event.name,
    event.begin, event.begin, color))

file.close()