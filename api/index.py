import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables
os.environ['MIMO_API_KEY'] = os.environ.get('MIMO_API_KEY', 'sk-sx5305wu8bb3usteoszw6yuhcl9474jmhxhp1vxef455rwyg')
os.environ['MIMO_API_URL'] = os.environ.get('MIMO_API_URL', 'https://api.xiaomimimo.com/v1')

from app import app

# Vercel expects the app to be named 'app'
application = app
