import os

#prod or local
is_prod = os.environ.get('IS_HEROKU', None)

# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
FLASK_DEBUG = True  # Do not use debug mode in production

# SQLAlchemy settings
if is_prod:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
	SQLALCHEMY_DATABASE_URI = 'postgresql://jsilva:jx3t2016@localhost/slidelate'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Files
UPLOAD_FOLDER = '/media/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])