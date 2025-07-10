from flask import Flask
from routes.query import query_bp
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Enable CORS for all origins during development.
# For production, you should restrict this to your frontend's domain:
# CORS(app, resources={r"/query": {"origins": "http://localhost:5173"}})
CORS(app)

# Register the blueprint for query-related routes
app.register_blueprint(query_bp)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)