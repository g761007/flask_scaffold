from __future__ import unicode_literals
# is the debug mode on
DEBUG = True

# !!!WARNING!!! MODIFY THIS IN PRODUCTION
SECRET_KEY = ''

# interface to bind
SERVER_HOSTNAME = '0.0.0.0'

# port to bind
SERVER_PORT = 5000

# should we use reloader to run the server
SERVER_USE_RELOADER = False

# should we use debugger to run the server
SERVER_USE_DEBUGGER = False

# URI of sqlite database
SQLITE_DATABASE_URI = ''
SQLITE_DATABASE_ECHO = False

# logging format to display
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

VERSION = '0.0.0'

#: API kyes
API_KEYS = set([
    '40b27e02d446ed1eca42dce3753cb46e3df82cae',
])