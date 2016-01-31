import sys
sys.path.insert(0, "/var/www/wsgi-scripts/")

from front import app
application = app
