# WSGI configuration for PythonAnywhere
import sys

project_home = '/home/Adul69/mimo-doc-writer'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

import os
os.environ['FLASK_ENV'] = 'production'

from app import app as application
