# from flask import Flask
# from routes.query import query_bp
# from flask_cors import CORS
# import os

# # Create a Flask application instance
# app = Flask(__name__)


# if os.environ.get("VERCEL"):
#     origins = "https://ai-database-editor.vercel.app"
# else:
#     origins = "*" 

# # Configure CORS
# CORS(app, resources={r"/*": {"origins": origins}})

# # Register the blueprint for query-related routes
# app.register_blueprint(query_bp)

# # Run the Flask application
# if __name__ == '__main__':
#     # Use the PORT environment variable if available, otherwise default to 5000
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)

from flask import Flask
from flask_cors import CORS
from routes.query import query_bp
import os
from datetime import timedelta

# Create a Flask application instance
app = Flask(__name__)

# Set a secret key for session management. In a real production app,
# this should be a long, random string stored securely as an environment variable.
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# Configure session settings for better security and persistence
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_TYPE'] = 'filesystem'  # Can be changed to 'redis' for production

# Enable CORS with credentials support
CORS(app, 
     supports_credentials=True,
     origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:3000', 'http://127.0.0.1:5173'],
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)

# Register the blueprint for all our application routes
app.register_blueprint(query_bp)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint to verify the server is running"""
    return {'status': 'healthy', 'message': 'AI Database Assistant is running'}, 200

# Root endpoint with API information
@app.route('/', methods=['GET'])
def root():
    """Root endpoint providing API information"""
    return {
        'name': 'AI Database Assistant API',
        'version': '1.0.0',
        'endpoints': {
            '/connect': 'POST - Connect to database',
            '/disconnect': 'POST - Disconnect from database',
            '/query': 'POST - Execute natural language query',
            '/history': 'GET - Get query history',
            '/revert': 'POST - Revert a database change',
            '/health': 'GET - Health check'
        }
    }, 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

# Run the Flask application
if __name__ == '__main__':
    # Check for required environment variables
    if not os.getenv('GEMINI_API_KEY'):
        print("WARNING: GEMINI_API_KEY not found in environment variables!")
        print("Please set it in your .env file or environment")
    
    # Run with debug mode for development
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        threaded=True
    )