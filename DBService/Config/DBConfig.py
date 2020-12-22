import os

DBCONFIG = {
    'DBNAME': 'MONGODB',
    'HOST'  : os.environ.get('MONGODB_HOST'),
    'PORT'  : os.environ.get('MONGODB_PORT'),
    'DATABASE': os.environ.get('MONGODB_DB'),
    'USERNAME': os.environ.get('MONGODB_USER'),
    'PASS': os.environ.get('MONGODB_PASS')
}
