from flask import Flask
from routes.query import query_bp
from flask_cors import CORS
import os

# Create a Flask application instance
app = Flask(__name__)


if os.environ.get("VERCEL"):
    origins = "https://ai-database-editor.vercel.app"
else:
    origins = "*" 

# Configure CORS
CORS(app, resources={r"/*": {"origins": origins}})

# Register the blueprint for query-related routes
app.register_blueprint(query_bp)

# Run the Flask application
if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
