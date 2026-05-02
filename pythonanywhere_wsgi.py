# WSGI configuration for PythonAnywhere
import sys
import os

project_home = '/home/Adul69/mimo-doc-writer'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables directly
os.environ['MIMO_API_KEY'] = 'sk-sx5305wu8bb3usteoszw6yuhcl9474jmhxhp1vxef455rwyg'
os.environ['MIMO_API_URL'] = 'https://api.xiaomimimo.com/v1'
os.environ['FLASK_ENV'] = 'production'

from app import app as application
