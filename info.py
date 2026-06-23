import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot information
SESSION = environ.get('SESSION', 'Rs_link_bots')
API_ID = int(environ.get('API_ID', '26069847')) ##api id fot t.me.org
API_HASH = environ.get('API_HASH', 'ae19bdc8f9e4ab74c59ff41877379db7') #api hash fot t.me.org
BOT_TOKEN = environ.get('BOT_TOKEN', "")

# Bot settings
PORT = environ.get("PORT", "8080") #your hosting site port or use default port

# Online Stream and Download
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "") #hosting site URL

# Admins, Channels & Users
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1004300066235')) #LOG channel id
ADMINS = [7927456122] #replace with your ID

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://budhamagarmadan37_db_user:TeovwrLEr3NcJ0Ye@cluster0.qfipr27.mongodb.net/?appName=Cluster0") #mongo DB URL
DATABASE_NAME = environ.get('DATABASE_NAME', "rs_fllink_bot")

# Shortlink Info
SHORTLINK = "False" # Set True Or False
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
SHORTLINK_API = environ.get('SHORTLINK_API', 'hRPS5vvZc0OGOEUQJMJzPiojoVK2')
