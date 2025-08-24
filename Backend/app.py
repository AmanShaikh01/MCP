from flask import Flask
from routes.query import query_bp
from flask_cors import CORS

# Create a Flask application instance
app = Flask(__name__)

# Define the allowed origin (your Vercel app's URL)
# REPLACE THIS with your actual Vercel URL
origins = "https://ai-database-editor.vercel.app/" 

# Configure CORS to only allow requests from your frontend
CORS(app, resources={r"/query*": {"origins": origins}})

# Register the blueprint for query-related routes
app.register_blueprint(query_bp)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
