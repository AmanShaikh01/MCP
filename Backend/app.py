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

# from flask import Flask
# from flask_cors import CORS
# from routes.query import query_bp
# import os
# from datetime import timedelta

# # Create a Flask application instance
# app = Flask(__name__)

# # Set a secret key for session management. In a real production app,
# # this should be a long, random string stored securely as an environment variable.
# app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
     
# # Configure session settings for better security and persistence
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
# app.config['SESSION_TYPE'] = 'filesystem'  # Can be changed to 'redis' for production

# Enable CORS with credentials support
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

# from flask import Flask
# from flask_cors import CORS
# from routes.query import query_bp
# import os
# from datetime import timedelta

# # Create a Flask application instance
# app = Flask(__name__)

# # Set a secret key for session management. In a real production app,
# # this should be a long, random string stored securely as an environment variable.
# app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# # Configure session settings for better security and persistence
# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
# app.config['SESSION_TYPE'] = 'filesystem'  # Can be changed to 'redis' for production

# Enable CORS with credentials support
# CORS(app,
#      supports_credentials=True,
#      origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:3000', 'http://127.0.0.1:5173', 'https://ai-database-editor.vercel.app/'],
#      allow_headers=['Content-Type', 'Authorization'],
#      methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
# )
# CORS(app,
#      supports_credentials=True,
#      origins=['https://ai-database-editor.vercel.app/'], # <-- IMPORTANT: Add your Vercel URL here
#      allow_headers=['Content-Type', 'Authorization'],
#      methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
# )

# # Register the blueprint for all our application routes
# app.register_blueprint(query_bp)

# # Health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     """Simple health check endpoint to verify the server is running"""
#     return {'status': 'healthy', 'message': 'AI Database Assistant is running'}, 200

# # Root endpoint with API information
# @app.route('/', methods=['GET'])
# def root():
#     """Root endpoint providing API information"""
#     return {
#         'name': 'AI Database Assistant API',
#         'version': '1.0.0',
#         'llm_provider': 'Groq (FREE)',
#         'endpoints': {
#             '/connect': 'POST - Connect to database',
#             '/disconnect': 'POST - Disconnect from database',
#             '/query': 'POST - Execute natural language query',
#             '/history': 'GET - Get query history',
#             '/revert': 'POST - Revert a database change',
#             '/health': 'GET - Health check'
#         }
#     }, 200

# # Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     return {'error': 'Endpoint not found'}, 404

# @app.errorhandler(500)
# def internal_error(error):
#     return {'error': 'Internal server error'}, 500

# # Run the Flask application
# if __name__ == '__main__':
#     # Check for required environment variables
#     groq_key = os.getenv('GROQ_API_KEY')
    
#     if not groq_key:
#         print("=" * 60)
#         print("⚠️  WARNING: GROQ_API_KEY not found!")
#         print("=" * 60)
#         print("\n📋 Setup Instructions:")
#         print("1. Go to: https://console.groq.com/keys")
#         print("2. Sign up for FREE and create an API key")
#         print("3. Add to your .env file:")
#         print("   GROQ_API_KEY=your_api_key_here")
#         print("\n💡 Groq Free Tier Limits:")
#         print("   - 30 requests per minute")
#         print("   - 14,400 requests per day")
#         print("   - ~20,000-30,000 tokens per minute")
#         print("=" * 60)
#         print("\n⚠️  Server will start but API calls will fail without the key!\n")
#     else:
#         print("=" * 60)
#         print("✅ GROQ_API_KEY found!")
#         print("=" * 60)
#         print(f"🔑 API Key: {groq_key[:10]}...{groq_key[-4:]}")
#         print("🤖 Model: llama-3.3-70b-versatile (FREE)")
#         print("⚡ Tool Calling: Enabled")
#         print("=" * 60)
#         print()
   
#     # Run with debug mode for development
#     print("🚀 Starting AI Database Editor Server...")
#     print("📍 Server: http://127.0.0.1:5000")
#     print("📍 Frontend: http://localhost:3000")
#     print("\n💡 Press CTRL+C to quit\n")
    
#     app.run(
#         debug=True,
#         host='0.0.0.0',
#         port=5000,
#         threaded=True
#     )

# # Register the blueprint for all our application routes
# app.register_blueprint(query_bp)

# # Health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     """Simple health check endpoint to verify the server is running"""
#     return {'status': 'healthy', 'message': 'AI Database Assistant is running'}, 200

# # Root endpoint with API information
# @app.route('/', methods=['GET'])
# def root():
#     """Root endpoint providing API information"""
#     return {
#         'name': 'AI Database Assistant API',
#         'version': '1.0.0',
#         'llm_provider': 'Groq (FREE)',
#         'endpoints': {
#             '/connect': 'POST - Connect to database',
#             '/disconnect': 'POST - Disconnect from database',
#             '/query': 'POST - Execute natural language query',
#             '/history': 'GET - Get query history',
#             '/revert': 'POST - Revert a database change',
#             '/health': 'GET - Health check'
#         }
#     }, 200

# # Error handlers
# @app.errorhandler(404)
# def not_found(error):
#     return {'error': 'Endpoint not found'}, 404

# @app.errorhandler(500)
# def internal_error(error):
#     return {'error': 'Internal server error'}, 500

# # Run the Flask application
# if __name__ == '__main__':
#     # Check for required environment variables
#     groq_key = os.getenv('GROQ_API_KEY')
    
#     if not groq_key:
#         print("=" * 60)
#         print("⚠️  WARNING: GROQ_API_KEY not found!")
#         print("=" * 60)
#         print("\n📋 Setup Instructions:")
#         print("1. Go to: https://console.groq.com/keys")
#         print("2. Sign up for FREE and create an API key")
#         print("3. Add to your .env file:")
#         print("   GROQ_API_KEY=your_api_key_here")
#         print("\n💡 Groq Free Tier Limits:")
#         print("   - 30 requests per minute")
#         print("   - 14,400 requests per day")
#         print("   - ~20,000-30,000 tokens per minute")
#         print("=" * 60)
#         print("\n⚠️  Server will start but API calls will fail without the key!\n")
#     else:
#         print("=" * 60)
#         print("✅ GROQ_API_KEY found!")
#         print("=" * 60)
#         print(f"🔑 API Key: {groq_key[:10]}...{groq_key[-4:]}")
#         print("🤖 Model: llama-3.3-70b-versatile (FREE)")
#         print("⚡ Tool Calling: Enabled")
#         print("=" * 60)
#         print()
   
#     # Run with debug mode for development
#     print("🚀 Starting AI Database Editor Server...")
#     print("📍 Server: http://127.0.0.1:5000")
#     print("📍 Frontend: http://localhost:3000")
#     print("\n💡 Press CTRL+C to quit\n")
    
#     app.run(
#         debug=True,
#         host='0.0.0.0',
#         port=5000,
#         threaded=True
#     )

from flask import Flask
from flask_cors import CORS
from routes.query import query_bp
import os
from datetime import timedelta

# 1. Create and Configure the Flask App
# ==================================================
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# Backend/app.py - NEW & IMPROVED CONFIGURATION

# Configure session cookie settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Production-specific cookie settings for cross-domain sessions
if os.getenv('RENDER'): # RENDER is an env var automatically set by Render.com
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
else:
    # Development settings (for localhost)
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False

# NEW DYNAMIC CORS CONFIGURATION
# This will read allowed URLs from an environment variable
origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

CORS(app,
     supports_credentials=True,
     origins=origins,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)

# 2. Register Blueprints
# ==================================================
# All routes from routes/query.py will be added to the app
app.register_blueprint(query_bp)


# 3. Define App-Level Routes (Health Check, Root)
# ==================================================
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint to verify the server is running"""
    return {'status': 'healthy', 'message': 'AI Database Assistant is running'}, 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint providing API information"""
    return {
        'name': 'AI Database Assistant API',
        'version': '1.0.0',
        'llm_provider': 'Groq (FREE)',
        'endpoints': {
            '/connect': 'POST - Connect to database',
            '/disconnect': 'POST - Disconnect from database',
            '/query': 'POST - Execute natural language query',
            '/history': 'GET - Get query history',
            '/revert': 'POST - Revert a database change',
            '/health': 'GET - Health check'
        }
    }, 200


# 4. Define Error Handlers
# ==================================================
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500


# 5. Run the Application
# ==================================================
if __name__ == '__main__':
    # Check for required environment variables
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key:
        print("=" * 60)
        print("⚠️  WARNING: GROQ_API_KEY not found!")
        print("=" * 60)
        print("\n📋 Setup Instructions:")
        print("1. Go to: https://console.groq.com/keys")
        print("2. Sign up for FREE and create an API key")
        print("3. Add to your .env file:")
        print("   GROQ_API_KEY=your_api_key_here")
        print("=" * 60)
        print("\n⚠️  Server will start but API calls will fail without the key!\n")
    else:
        print("=" * 60)
        print("✅ GROQ_API_KEY found!")
        print("=" * 60)

    print("🚀 Starting AI Database Editor Server...")
    print("📍 Server: http://127.0.0.1:5000")
    print("📍 Frontend: http://localhost:3000")
    print("\n💡 Press CTRL+C to quit\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
