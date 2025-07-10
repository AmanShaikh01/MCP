# Fixed routes/query.py
from flask import Blueprint, request, jsonify
from utils.llm import run_llm_query
from utils.db import get_students

# Create a Blueprint named 'query'
query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query():
    """
    Handles POST requests to the /query endpoint.
    Expects a JSON payload with a 'query' field containing the user's natural language request.
    Uses the LLM to process the request and interact with the database.
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        user_input = data.get('query')
        response = run_llm_query(user_input)
        return jsonify({'response': response})
    except Exception as e:
        # Catch any exceptions during processing and return an 'error' message
        return jsonify({'error': str(e)}), 500

@query_bp.route('/test-db', methods=['GET'])
def test_db():
    """
    Handles GET requests to the /test-db endpoint.
    This route is for testing the Supabase database connection and fetching
    some basic statistics about the student data.
    """
    try:
        students = get_students()
        # Check if get_students returned an error string
        if isinstance(students, str) and students.startswith("Error"):
            return jsonify({'error': students}), 500
        
        # If students is a list, proceed to extract useful information
        if isinstance(students, list):
            # Get unique department names from the student data
            departments = list(set([s.get('department') for s in students if s.get('department')]))
            
            # Extract CGPA values and calculate basic statistics
            cgpas = [s.get('cgpa') for s in students if s.get('cgpa') is not None]
            cgpa_stats = {
                'min': min(cgpas) if cgpas else None,
                'max': max(cgpas) if cgpas else None,
                'count_above_8': len([c for c in cgpas if c > 8]) if cgpas else 0
            }
            
            # Return a success message with database statistics
            return jsonify({
                'message': 'Database connection successful',
                'total_students': len(students),
                'departments': departments,
                'cgpa_stats': cgpa_stats,
                'sample_data': students[:2] if students else []
            })
        else:
            # Handle unexpected return type from get_students
            return jsonify({'error': 'Unexpected data type from database. Check db.py.'}), 500
    except Exception as e:
        # Catch any exceptions during processing and return an 'error' message
        return jsonify({'error': str(e)}), 500