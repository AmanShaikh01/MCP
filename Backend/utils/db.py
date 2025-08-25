import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Any, Union

# Load environment variables
load_dotenv()

# --- Supabase Client Initialization ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("DEBUG: Supabase client initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize Supabase client: {e}")
    raise

def get_students() -> Union[List[Dict[str, Any]], str]:
    """Retrieves all students from the database."""
    try:
        response = supabase.from_('students').select('*').execute()
        if response.data is None:
            return "Error: No data received from Supabase for get_students."
        return response.data
    except Exception as e:
        error_msg = f"Error in get_students: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg

def dynamic_student_query(filters: Dict[str, Dict[str, Union[str, float, int]]]) -> Union[List[Dict[str, Any]], str]:
    """
    Queries students based on dynamic filters.
    Filters example: {'department': {'op': 'eq', 'value': 'Computer Science'}, 'cgpa': {'op': 'gte', 'value': 8.5}}
    """
    try:
        query = supabase.from_('students').select('*')

        for column, condition in filters.items():
            op = condition.get('op')
            value = condition.get('value')

            if op == 'eq':
                query = query.eq(column, value)
            elif op == 'gt':
                query = query.gt(column, value)
            elif op == 'lt':
                query = query.lt(column, value)
            elif op == 'gte':
                query = query.gte(column, value)
            elif op == 'lte':
                query = query.lte(column, value)
            elif op == 'like':
                query = query.like(column, f'%{value}%')
            else:
                print(f"WARNING: Unsupported operator '{op}' for column '{column}'. Skipping filter.")
                continue

        response = query.execute()
        if response.data is None:
            return "Error: No data received from Supabase for dynamic_student_query."
        return response.data
    except Exception as e:
        error_msg = f"Error in dynamic_student_query with filters {filters}: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg

def add_student(student_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
    """Adds a new student record to the database."""
    try:
        response = supabase.from_('students').insert(student_data).execute()
        if response.data is None or not response.data:
            return "Error: No data returned after insert. Student might not have been added."
        return response.data[0]
    except Exception as e:
        error_msg = f"Error in add_student with data {student_data}: {e}"
        print(f"ERROR: {error_msg}")
        if "duplicate key value violates unique constraint" in str(e):
            return "Error: A student with this roll number or email already exists."
        return error_msg

def update_student(filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
    """Updates existing student record(s) based on filters."""
    try:
        # Start the query chain with update()
        query = supabase.from_('students').update(new_data)
        # Chain filtering methods after update()
        for column, value in filters.items():
            query = query.eq(column, value)
        
        response = query.execute()
        if response.data is None:
            return "Error: No data received from Supabase after update."
        return response.data
    except Exception as e:
        error_msg = f"Error in update_student with filters {filters} and new_data {new_data}: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg

def delete_student(filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
    """Deletes student record(s) based on filters."""
    try:
        # Start the query chain with delete()
        query = supabase.from_('students').delete()
        # Chain filtering methods after delete()
        for column, value in filters.items():
            query = query.eq(column, value)
        
        response = query.execute()
        if response.data is None:
            return "Error: No data received from Supabase after delete."
        return response.data
    except Exception as e:
        error_msg = f"Error in delete_student with filters {filters}: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg