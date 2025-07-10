import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import BaseOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from typing import List, Dict, Union, Any

# Import database interaction functions
from utils.db import (
    dynamic_student_query, get_students,
    add_student, update_student, delete_student
)

# Load environment variables from .env file
load_dotenv()

class QueryClassifier:
    """Classifies user queries into CRUD operations"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def classify_query(self, query: str) -> str:
        """Classify the query into one of: query, add, update, delete"""
        prompt = f"""
        Classify the following user query into one of these categories:
        - "query": For searching, finding, listing, or retrieving student information
        - "add": For adding, creating, or inserting new student records
        - "update": For modifying, changing, or updating existing student information
        - "delete": For removing, deleting, or eliminating student records
        
        User query: "{query}"
        
        Return only one word: query, add, update, or delete
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            classification = response.content.strip().lower()
            
            if classification in ['query', 'add', 'update', 'delete']:
                return classification
            else:
                return 'query'  # Default to query if unclear
        except Exception as e:
            print(f"Error in classify_query: {e}")
            return 'query'  # Default fallback

def get_database_schema_info():
    """
    Fetches basic schema information from the database to help the LLM.
    """
    try:
        students = get_students()
        if isinstance(students, list) and students:
            departments = list(set([s.get('department') for s in students if s.get('department')]))
            sample_student = students[0] if students else {}
            return {
                'departments': departments,
                'sample_columns': list(sample_student.keys()) if sample_student else [],
                'total_count': len(students)
            }
        return {'departments': [], 'sample_columns': [], 'total_count': 0}
    except Exception as e:
        print(f"ERROR: Error getting database schema info: {e}")
        return {'departments': [], 'sample_columns': [], 'total_count': 0}

def get_llm():
    """Returns a configured ChatGoogleGenerativeAI instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY must be set in environment variables")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.1
    )

def clean_json_output(text: str) -> str:
    """Clean JSON output from LLM response"""
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    text = text.strip()
    
    # Find JSON object in the text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return text

def handle_query_operation(user_query: str, llm) -> str:
    """Handle database query operations"""
    try:
        db_info = get_database_schema_info()
        
        # First, determine what type of information the user wants
        intent_prompt = f"""
        Analyze this query and determine what specific information the user wants:
        
        Query: "{user_query}"
        
        Choose one of these response types:
        - "count": User wants just a number/count (e.g., "how many", "count of")
        - "list": User wants to see actual student records
        - "summary": User wants aggregated information (e.g., average, statistics)
        
        Return only one word: count, list, or summary
        """
        
        intent_response = llm.invoke([HumanMessage(content=intent_prompt)])
        intent = intent_response.content.strip().lower()
        
        prompt = f"""
        Extract database filter conditions from this student query.
        
        Available departments: {db_info['departments']}
        Available columns: {db_info['sample_columns']}
        
        IMPORTANT: Use exact department names from the list above.
        For department queries, map common terms:
        - "computer", "cs", "computer science" -> "Computer"
        - "mechanical", "mech" -> "Mechanical"
        - "electrical", "ee" -> "Electrical"
        - etc.
        
        Common column mappings:
        - "gpa", "cgpa" -> "cgpa"
        - "department" -> "department"
        - "name" -> "name"
        - "roll number" -> "roll_number"
        
        Operators: eq, gt, lt, gte, lte, like
        
        Query: "{user_query}"
        
        Return JSON format:
        {{"filters": {{"column_name": {{"op": "operator", "value": "value"}}}}}}
        
        If no specific filters, return: {{"filters": {{}}}}
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned_response = clean_json_output(response.content)
        
        try:
            parsed = json.loads(cleaned_response)
            filters = parsed.get('filters', {})
            
            if not filters:
                # Return all students but format based on intent
                students = get_students()
                if isinstance(students, list) and students:
                    if intent == "count":
                        return f"Total number of students: {len(students)}"
                    elif intent == "summary":
                        return f"Total students: {len(students)}\nDepartments: {', '.join(db_info['departments'])}"
                    else:  # list
                        if len(students) > 5:
                            return f"Found {len(students)} students. Here are the first 5:\n{json.dumps(students[:5], indent=2)}"
                        else:
                            return f"Found {len(students)} student(s):\n{json.dumps(students, indent=2)}"
                return "No students found in database."
            
            result = dynamic_student_query(filters)
            
            if isinstance(result, str) and result.startswith("Error"):
                return f"Database error: {result}"
            
            if not result:
                return "No students found matching your criteria."
            
            # Format response based on user intent
            if intent == "count":
                # Extract what they're counting from the query
                if any(word in user_query.lower() for word in ["how many", "count", "number of"]):
                    if "department" in filters or "computer" in user_query.lower():
                        dept_name = filters.get('department', {}).get('value', 'Computer')
                        return f"Number of students in {dept_name} department: {len(result)}"
                    else:
                        return f"Number of students matching criteria: {len(result)}"
                        
            elif intent == "summary":
                # Provide summary statistics
                if len(result) == 1:
                    return f"Found 1 student:\n{json.dumps(result[0], indent=2)}"
                else:
                    avg_cgpa = sum(s.get('cgpa', 0) for s in result if s.get('cgpa')) / len([s for s in result if s.get('cgpa')])
                    return f"Found {len(result)} students.\nAverage CGPA: {avg_cgpa:.2f}\nFirst student: {result[0].get('name', 'N/A')}"
                    
            else:  # list - show actual records
                if len(result) > 5:
                    return f"Found {len(result)} students. Here are the first 5:\n{json.dumps(result[:5], indent=2)}"
                else:
                    return f"Found {len(result)} student(s):\n{json.dumps(result, indent=2)}"
                
        except json.JSONDecodeError as e:
            return f"Error parsing query filters: {e}. Raw response: {cleaned_response}"
            
    except Exception as e:
        return f"Error processing query: {str(e)}"

def handle_add_operation(user_query: str, llm) -> str:
    """Handle add student operations"""
    try:
        prompt = f"""
        Extract student data from this request to add a new student.
        
        Request: "{user_query}"
        
        Return JSON format:
        {{"student_data": {{"name": "value", "roll_number": "value", "department": "value", "cgpa": 0.0}}}}
        
        Include all available information. At minimum need name and roll_number.
        If insufficient info, return: {{"student_data": {{}}}}
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned_response = clean_json_output(response.content)
        
        try:
            parsed = json.loads(cleaned_response)
            student_data = parsed.get('student_data', {})
            
            if not student_data or 'name' not in student_data or 'roll_number' not in student_data:
                return "To add a student, I need at least their name and roll number. Please provide both."
            
            result = add_student(student_data)
            
            if isinstance(result, str) and result.startswith("Error"):
                return f"Error adding student: {result}"
            
            return f"Successfully added student: {result.get('name', 'N/A')} (Roll No: {result.get('roll_number', 'N/A')})"
            
        except json.JSONDecodeError as e:
            return f"Error parsing add data: {e}. Raw response: {cleaned_response}"
            
    except Exception as e:
        return f"Error processing add request: {str(e)}"

def handle_update_operation(user_query: str, llm) -> str:
    """Handle update student operations"""
    try:
        prompt = f"""
        Extract filters and new data from this update request.
        
        Request: "{user_query}"
        
        Return JSON format:
        {{"filters": {{"roll_number": "value"}}, "new_data": {{"column": "new_value"}}}}
        
        Use roll_number or email for unique identification.
        If unclear, return: {{"filters": {{}}, "new_data": {{}}}}
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned_response = clean_json_output(response.content)
        
        try:
            parsed = json.loads(cleaned_response)
            filters = parsed.get('filters', {})
            new_data = parsed.get('new_data', {})
            
            if not filters or not new_data:
                return "Please specify both which student to update and what data to change."
            
            result = update_student(filters, new_data)
            
            if isinstance(result, str) and result.startswith("Error"):
                return f"Error updating student: {result}"
            
            if not result:
                return "No student found matching the criteria for update."
            
            return f"Successfully updated {len(result)} student(s)."
            
        except json.JSONDecodeError as e:
            return f"Error parsing update data: {e}. Raw response: {cleaned_response}"
            
    except Exception as e:
        return f"Error processing update request: {str(e)}"

def handle_delete_operation(user_query: str, llm) -> str:
    """Handle delete student operations"""
    try:
        prompt = f"""
        Extract filters from this delete request.
        
        Request: "{user_query}"
        
        Return JSON format:
        {{"filters": {{"roll_number": "value"}}}}
        
        Use roll_number or email for unique identification.
        If unclear, return: {{"filters": {{}}}}
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        cleaned_response = clean_json_output(response.content)
        
        try:
            parsed = json.loads(cleaned_response)
            filters = parsed.get('filters', {})
            
            if not filters:
                return "Please specify which student to delete using roll number or email."
            
            result = delete_student(filters)
            
            if isinstance(result, str) and result.startswith("Error"):
                return f"Error deleting student: {result}"
            
            if not result:
                return "No student found matching the criteria for deletion."
            
            return f"Successfully deleted {len(result)} student(s)."
            
        except json.JSONDecodeError as e:
            return f"Error parsing delete filters: {e}. Raw response: {cleaned_response}"
            
    except Exception as e:
        return f"Error processing delete request: {str(e)}"

def run_llm_query(user_query: str) -> str:
    """
    Main function to process user queries using LLM without complex agents
    """
    try:
        llm = get_llm()
        classifier = QueryClassifier(llm)
        
        # Classify the query
        operation = classifier.classify_query(user_query)
        print(f"DEBUG: Classified operation: {operation}")
        
        # Route to appropriate handler
        if operation == 'add':
            return handle_add_operation(user_query, llm)
        elif operation == 'update':
            return handle_update_operation(user_query, llm)
        elif operation == 'delete':
            return handle_delete_operation(user_query, llm)
        else:  # Default to query
            return handle_query_operation(user_query, llm)
            
    except Exception as e:
        print(f"Error in run_llm_query: {str(e)}")
        return f"Error processing your request: {str(e)}. Please try again or rephrase your query."