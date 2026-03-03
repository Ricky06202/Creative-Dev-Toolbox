import sys
import os

# Add the current directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    # Lazy loading of a2wsgi for cPanel stability
    from a2wsgi import ASGIMiddleware
    from main import app
    
    # Wrap the FastAPI app
    wsgi_app = ASGIMiddleware(app)
    return wsgi_app(environ, start_response)
