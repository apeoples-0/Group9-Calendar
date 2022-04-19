import datetime

# Account info for MySQL database
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '1234'
MYSQL_DB = 'webcalendar'

# Flask Secret Key
SECRET_KEY = 'A secret key.'

# Flask Session Time (for retaining user logins) (Users will remain logged in for 14 days)
PERMANENT_SESSION_LIFETIME = datetime.timedelta(14)

# Calendar Configuration
HOLIDAY_COLOR = 'black'