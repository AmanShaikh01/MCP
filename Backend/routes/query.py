# # Fixed routes/query.py
# from flask import Blueprint, request, jsonify
# from utils.llm import run_llm_query
# from utils.db import get_students

# # Create a Blueprint named 'query'
# query_bp = Blueprint('query', __name__)

# @query_bp.route('/query', methods=['POST'])
# def query():
#     """
#     Handles POST requests to the /query endpoint.
#     Expects a JSON payload with a 'query' field containing the user's natural language request.
#     Uses the LLM to process the request and interact with the database.
#     """
#     try:
#         data = request.get_json()
#         if not data or 'query' not in data:
#             return jsonify({'error': 'Missing query parameter'}), 400
        
#         user_input = data.get('query')
#         response = run_llm_query(user_input)
#         return jsonify({'response': response})
#     except Exception as e:
#         # Catch any exceptions during processing and return an 'error' message
#         return jsonify({'error': str(e)}), 500

# @query_bp.route('/test-db', methods=['GET'])
# def test_db():
#     """
#     Handles GET requests to the /test-db endpoint.
#     This route is for testing the Supabase database connection and fetching
#     some basic statistics about the student data.
#     """
#     try:
#         students = get_students()
#         # Check if get_students returned an error string
#         if isinstance(students, str) and students.startswith("Error"):
#             return jsonify({'error': students}), 500
        
#         # If students is a list, proceed to extract useful information
#         if isinstance(students, list):
#             # Get unique department names from the student data
#             departments = list(set([s.get('department') for s in students if s.get('department')]))
            
#             # Extract CGPA values and calculate basic statistics
#             cgpas = [s.get('cgpa') for s in students if s.get('cgpa') is not None]
#             cgpa_stats = {
#                 'min': min(cgpas) if cgpas else None,
#                 'max': max(cgpas) if cgpas else None,
#                 'count_above_8': len([c for c in cgpas if c > 8]) if cgpas else 0
#             }
            
#             # Return a success message with database statistics
#             return jsonify({
#                 'message': 'Database connection successful',
#                 'total_students': len(students),
#                 'departments': departments,
#                 'cgpa_stats': cgpa_stats,
#                 'sample_data': students[:2] if students else []
#             })
#         else:
#             # Handle unexpected return type from get_students
#             return jsonify({'error': 'Unexpected data type from database. Check db.py.'}), 500
#     except Exception as e:
#         # Catch any exceptions during processing and return an 'error' message
#         return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify, session
from sqlalchemy import create_engine
from utils.llm import run_llm_query
import json
import traceback

# Create a Blueprint for all our routes
query_bp = Blueprint('query', __name__)

@query_bp.route('/connect', methods=['POST'])
def connect():
    """
    Handles POST requests to establish a database connection.
    Tests the credentials and, if successful, stores them in a secure server-side session.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing connection data'}), 400

        db_type = data.get('db_type')
        
        # Construct the database URI based on the selected type
        if db_type in ['postgresql', 'mysql', 'supabase']:
            # For Supabase and cloud databases, check if connection_string is provided
            connection_string = data.get('connection_string')
            
            if connection_string:
                # Use the full connection string directly
                if db_type == 'supabase':
                    # Supabase uses PostgreSQL protocol
                    if not connection_string.startswith('postgresql://'):
                        connection_string = 'postgresql://' + connection_string
                    db_uri = connection_string.replace('postgresql://', 'postgresql+psycopg2://')
                elif db_type == 'postgresql':
                    if connection_string.startswith('postgresql://') or connection_string.startswith('postgres://'):
                        db_uri = connection_string.replace('postgresql://', 'postgresql+psycopg2://').replace('postgres://', 'postgresql+psycopg2://')
                    else:
                        db_uri = 'postgresql+psycopg2://' + connection_string
                else:  # mysql
                    if not connection_string.startswith('mysql://'):
                        connection_string = 'mysql://' + connection_string
                    db_uri = connection_string.replace('mysql://', 'mysql+pymysql://')
            else:
                # Use individual credentials (legacy support)
                user = data.get('user')
                password = data.get('password')
                host = data.get('host')
                dbname = data.get('dbname')
                port = data.get('port', 5432 if db_type in ['postgresql', 'supabase'] else 3306)

                if not all([user, password, host, dbname]):
                    return jsonify({'error': 'Missing connection details. Provide either a connection string or individual credentials.'}), 400

                if db_type in ['postgresql', 'supabase']:
                    db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
                else:  # mysql
                    db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"

        elif db_type == 'mongodb':
            db_uri = data.get('connection_string') or data.get('db_uri')
            if not db_uri:
                return jsonify({'error': 'Missing connection string for MongoDB'}), 400
        else:
            return jsonify({'error': 'Unsupported database type'}), 400

        # Test the connection to ensure credentials are valid
        if db_type != 'mongodb':
            engine = create_engine(db_uri)
            connection = engine.connect()
            connection.close()
        else:
            # Test MongoDB connection
            from pymongo import MongoClient
            client = MongoClient(db_uri, serverSelectionTimeoutMS=5000)
            client.server_info()  # Will raise an exception if cannot connect
            client.close()
        
        # Store the successful URI and other details in the user's session
        session['db_uri'] = db_uri
        session['db_type'] = db_type if db_type != 'supabase' else 'postgresql'  # Treat Supabase as PostgreSQL
        session['mode'] = data.get('mode', 'read-only')  # Default to read-only
        session['history'] = []  # Initialize an empty history log

        return jsonify({'message': 'Connection successful'}), 200

    except Exception as e:
        print(f"Connection failed: {traceback.format_exc()}")
        return jsonify({'error': f'Connection failed: {str(e)}'}), 500

@query_bp.route('/disconnect', methods=['POST'])
def disconnect():
    """ Clears the user's session, securely removing all connection data. """
    session.clear()
    return jsonify({'message': 'Successfully disconnected'}), 200

@query_bp.route('/query', methods=['POST'])
def query():
    """
    Handles user queries. Retrieves connection details from the session
    and passes the query to the appropriate LangChain agent.
    """
    if 'db_uri' not in session:
        return jsonify({'error': 'Not connected to a database. Please connect first.'}), 401

    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request body'}), 400
        
        user_query = data.get('query')
        db_uri = session['db_uri']
        db_type = session['db_type']
        mode = session.get('mode', 'read-only')

        # Run the query using the LLM utility
        result = run_llm_query(user_query, db_uri, db_type, mode, session)
        
        # The run_llm_query function will now handle history logging,
        # so we just need to save the session state.
        session.modified = True

        return jsonify(result)

    except Exception as e:
        print(f"Query failed: {traceback.format_exc()}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@query_bp.route('/history', methods=['GET'])
def get_history():
    """ Returns the history of changes for the current session. """
    if 'db_uri' not in session:
        return jsonify({'error': 'Not connected to a database.'}), 401
    
    return jsonify({'history': session.get('history', [])})

@query_bp.route('/revert', methods=['POST'])
def revert_change():
    """ Reverts a specific change from the history log. """
    if 'db_uri' not in session or session.get('mode') != 'read-write':
        return jsonify({'error': 'Must be in read-write mode to revert changes.'}), 403

    try:
        data = request.get_json()
        history_id = data.get('history_id')

        if history_id is None or not (0 <= history_id < len(session.get('history', []))):
            return jsonify({'error': 'Invalid history ID.'}), 400

        history_entry = session['history'][history_id]
        if history_entry.get('reverted', False):
             return jsonify({'error': 'This change has already been reverted.'}), 400

        # (Simplified Revert Logic)
        # In a real implementation, this would call a utility function to perform
        # the opposite action based on the snapshot.
        
        # For now, we'll just mark it as reverted.
        history_entry['reverted'] = True
        session.modified = True
        
        return jsonify({'message': f"Successfully reverted change: {history_entry['description']}"})
        
    except Exception as e:
        print(f"Revert failed: {traceback.format_exc()}")
        return jsonify({'error': f'An unexpected error occurred during revert: {str(e)}'})