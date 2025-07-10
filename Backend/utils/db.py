# import os
# from supabase import create_client
# from dotenv import load_dotenv

# load_dotenv()

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# try:
#     supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# except Exception as e:
#     print(f"Error initializing Supabase client: {e}")
#     supabase = None # Handle case where client cannot be created

# def get_students():
#     """Fetches all students."""
#     if not supabase:
#         return "Error: Supabase client not initialized."
#     try:
#         response = supabase.table("students").select("*").execute()
#         return response.data
#     except Exception as e:
#         return f"Error fetching students: {str(e)}"

# def dynamic_student_query(filters):
#     """
#     Dynamically queries students based on filters.
#     filters: dict of column -> operation and value
#     Example: {
#                 "department":{"op":"eq","value":"CO"},
#                 "cgpa":{"op":"gt","value":8}
#     }
#     """
#     if not supabase:
#         return "Error: Supabase client not initialized."
#     try:
#         query = supabase.table("students").select("*")

#         for col, condition in filters.items():
#             op = condition.get("op")
#             value = condition.get("value")

#             if op == "eq":
#                 query = query.eq(col, value)
#             elif op == "gt":
#                 query = query.gt(col, value)
#             elif op == "lt":
#                 query = query.lt(col, value)
#             elif op == "gte":
#                 query = query.gte(col, value)
#             elif op == "lte":
#                 query = query.lte(col, value)
#             elif op == "like":
#                 query = query.like(col, f"%{value}%")
#             # Add more operations as needed (e.g., in, not_eq, is_null)
        
#         res = query.execute()
#         return res.data
#     except Exception as e:
#         return f"Error performing dynamic query: {str(e)}"

# def add_student(student_data):
#     """
#     Adds a new student record.
#     student_data: dict containing student details (e.g., {"name": "Alice", "department": "Computer"})
#     """
#     if not supabase:
#         return "Error: Supabase client not initialized."
#     try:
#         response = supabase.table("students").insert(student_data).execute()
#         # Supabase insert returns the inserted data in response.data[0]
#         return response.data[0] if response.data else "Student added successfully (no data returned)"
#     except Exception as e:
#         return f"Error adding student: {str(e)}"

# def update_student(filters, new_data):
#     """
#     Updates student records matching the filters with new_data.
#     filters: dict for filtering students (e.g., {"roll_number": "R001"})
#     new_data: dict of column -> new_value (e.g., {"cgpa": 9.2, "department": "Data Science"})
#     """
#     if not supabase:
#         return "Error: Supabase client not initialized."
#     try:
#         # First, ensure that filters uniquely identify the student(s) to avoid mass updates
#         # For this project, let's assume `roll_number` is unique for updates.
#         # You might need to adjust this based on your actual data schema and how users will identify students for updates.
#         if "roll_number" in filters:
#             response = supabase.table("students").update(new_data).eq("roll_number", filters["roll_number"]).execute()
#         elif "email" in filters: # Another common unique identifier
#             response = supabase.table("students").update(new_data).eq("email", filters["email"]).execute()
#         elif "name" in filters and "department" in filters:
#             # Potentially ambiguous, but might be acceptable depending on context.
#             response = supabase.table("students").update(new_data).eq("name", filters["name"]).eq("department", filters["department"]).execute()
#         else:
#             return "Error: Please provide a unique identifier (like roll_number or email) or specific combination (name and department) for updating a student."

#         return response.data
#     except Exception as e:
#         return f"Error updating student: {str(e)}"

# def delete_student(filters):
#     """
#     Deletes student records matching the filters.
#     filters: dict for filtering students (e.g., {"roll_number": "R001"})
#     """
#     if not supabase:
#         return "Error: Supabase client not initialized."
#     try:
#         if "roll_number" in filters:
#             response = supabase.table("students").delete().eq("roll_number", filters["roll_number"]).execute()
#         elif "email" in filters:
#             response = supabase.table("students").delete().eq("email", filters["email"]).execute()
#         elif "name" in filters and "department" in filters:
#             response = supabase.table("students").delete().eq("name", filters["name"]).eq("department", filters["department"]).execute()
#         else:
#             return "Error: Please provide a unique identifier (like roll_number or email) or specific combination (name and department) for deleting a student."

#         return response.data
#     except Exception as e:
#         return f"Error deleting student: {str(e)}"

# Fixed utils/db.py - SUPABASE INTERFACE WITH ENHANCED ERROR HANDLING
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
        query = supabase.from_('students')
        for column, value in filters.items():
            query = query.eq(column, value)
        
        response = query.update(new_data).execute()
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
        query = supabase.from_('students')
        for column, value in filters.items():
            query = query.eq(column, value)
        
        response = query.delete().execute()
        if response.data is None:
            return "Error: No data received from Supabase after delete."
        return response.data
    except Exception as e:
        error_msg = f"Error in delete_student with filters {filters}: {e}"
        print(f"ERROR: {error_msg}")
        return error_msg