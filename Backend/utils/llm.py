# import os
# import json
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import Tool, initialize_agent, AgentType
# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser # Corrected import path
# from langchain_core.pydantic_v1 import BaseModel, Fieldx    
# from typing import List, Dict, Union, Any

# from utils.db import (
#     dynamic_student_query, get_students,
#     add_student, update_student, delete_student
# )

# load_dotenv()

# # --- Helper to get Database Schema Info (unchanged from your version) ---
# def get_database_schema_info():
#     """Get actual data from database to help with query parsing."""
#     try:
#         students = get_students()
#         if isinstance(students, list) and students:
#             departments = list(set([s.get('department') for s in students if s.get('department')]))
#             sample_student = students[0] if students else {}
#             return {
#                 'departments': departments,
#                 'sample_columns': list(sample_student.keys()) if sample_student else [],
#                 'total_count': len(students)
#             }
#     except Exception as e:
#         print(f"Error getting database schema info: {e}")
#         pass
#     return {'departments': [], 'sample_columns': [], 'total_count': 0}

# # --- Pydantic Models for Output Parsing (Crucial for structured output) ---

# # Schema for parsing query filters
# class QueryFilters(BaseModel):
#     filters: Dict[str, Dict[str, Union[str, float, int]]] = Field(
#         description="A dictionary of filters for student queries, where keys are column names and values are dictionaries with 'op' (operation like eq, gt, lt, gte, lte, like) and 'value'."
#     )

# # Schema for parsing add student data
# class AddStudentData(BaseModel):
#     student_data: Dict[str, Any] = Field(
#         description="A dictionary containing key-value pairs for new student data. Keys must be exact column names. At least 'name' and 'roll_number' should be present."
#     )

# # Schema for parsing update student data
# class UpdateStudentData(BaseModel):
#     filters: Dict[str, Any] = Field(
#         description="A dictionary of filters to identify the student(s) to update. Use unique identifiers like 'roll_number' or 'email'.",
#         examples=[{"roll_number": "R123"}, {"name": "John Doe", "department": "Computer"}]
#     )
#     new_data: Dict[str, Any] = Field(
#         description="A dictionary of new data to apply to the matching student(s). Keys must be exact column names."
#     )

# # Schema for parsing delete student data
# class DeleteStudentData(BaseModel):
#     filters: Dict[str, Any] = Field(
#         description="A dictionary of filters to identify the student(s) to delete. Use unique identifiers like 'roll_number' or 'email'."
#     )

# # --- LLM for Intent Recognition and Parameter Extraction ---
# def get_llm():
#     """Returns a configured ChatGoogleGenerativeAI instance."""
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash-preview-05-20", # Updated model name
#         google_api_key=os.getenv("GEMINI_API_KEY"),
#         temperature=0.2 # Slightly higher temperature for more flexibility in parsing
#     )

# # --- Tool Definitions ---

# def build_student_query_tool():
#     """Tool for querying student data."""
#     # Use Pydantic parser for structured output
#     parser = JsonOutputParser(pydantic_object=QueryFilters)

#     # Prompt to guide the LLM to extract query filters
#     prompt = PromptTemplate.from_template("""
#         You are an assistant that extracts database filter conditions from natural language queries about students.
        
#         ACTUAL DATABASE INFO (if available):
#         - Available departments: {departments}
#         - Total students in database: {total_count}
#         - Sample columns: {sample_columns}
        
#         IMPORTANT MAPPING RULES for filters:
#         - For department queries, use EXACT department names from the available list above
#         - "Computer" or "CS" or "Computer Science" → use "Computer" if it's in the list
#         - "Data Science" or "DS" → use "Data Science" if it's in the list  
#         - "AI ML" or "AI" or "Machine Learning" → use "AI ML" if it's in the list
        
#         FIELD NAME MAPPINGS (use the correct column name from sample_columns):
#         - "backlogs" or "failed courses" or "failed_courses" → use "backlogs"
#         - "gpa" or "cgpa" or "grade point" → use "cgpa"
#         - "internship" → use "internship_status"
#         - "scholarship" → use "scholarship_status"
#         - "placement" → use "placement_status"
#         - "probation" → use "academic_probation"
#         - "projects" → use "projects_completed"
#         - "hackathons" → use "hackathons_participated"
        
#         Available operations: eq, gt, lt, gte, lte, like (for partial matches, e.g., name like 'john%')
        
#         CRITICAL: 
#         - Always use "cgpa" for GPA/CGPA queries.
#         - Use exact department names from the available list.
#         - If query cannot be converted to filters, return an empty filters dictionary: {{"filters": {{}}}}
#         - Provide the response in JSON format according to the schema below.
        
#         Schema:
#         {format_instructions}
        
#         Query: {query}
#         """)

#     chain = prompt | get_llm() | parser

#     def _run(input_query: str):
#         try:
#             db_info = get_database_schema_info()
            
#             # Prepare format instructions for the parser
#             format_instructions = parser.get_format_instructions()

#             response = chain.invoke({
#                 "query": input_query,
#                 "departments": db_info['departments'],
#                 "total_count": db_info['total_count'],
#                 "sample_columns": db_info['sample_columns'],
#                 "format_instructions": format_instructions
#             })
            
#             filters = response.get('filters', {})
#             print(f"DEBUG: Parsed query filters: {filters}")
            
#             if not filters:
#                 # If no filters, try to provide helpful info or default to all students
#                 students = get_students()
#                 if isinstance(students, list) and students:
#                     return f"I couldn't parse your query for specific filters. Available departments are: {db_info['departments']}. You can also ask for all students. Here are the first 2 students to give you an idea of the data:\n{json.dumps(students[:2], indent=2)}"
#                 return "Sorry, I couldn't understand your query. Please try rephrasing."
            
#             result = dynamic_student_query(filters)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return f"Database error during query: {result}"
            
#             if not result:
#                 return "No students found matching your criteria. Try adjusting your search terms or asking about available departments."
            
#             if len(result) > 5:
#                 sample_results = result[:5]
#                 return f"Found {len(result)} students. Here are the first 5:\n{json.dumps(sample_results, indent=2)}\n\n(Showing 5 of {len(result)} results)"
#             else:
#                 return f"Found {len(result)} student(s):\n{json.dumps(result, indent=2)}"
                
#         except Exception as e:
#             print(f"DEBUG: Exception in build_student_query_tool: {str(e)}")
#             return f"Error processing query request: {str(e)}"
    
#     return Tool(
#         name="QueryStudentDatabase",
#         func=_run,
#         description=(
#             "Use this tool to search for students in the database. "
#             "It understands queries about department, CGPA, attendance, name, etc. "
#             "Input should be the natural language query about what students to find."
#         )
#     )

# def build_add_student_tool():
#     """Tool for adding a new student."""
#     parser = JsonOutputParser(pydantic_object=AddStudentData)

#     prompt = PromptTemplate.from_template("""
#         You are an assistant that extracts new student data from natural language requests to add a student.
        
#         ACTUAL DATABASE INFO (if available):
#         - Sample columns: {sample_columns}
        
#         CRITICAL: 
#         - Extract all relevant information for a new student record.
#         - The 'roll_number' is typically a required and unique identifier for adding a student.
#         - Ensure data types match expected values (e.g., numbers for CGPA, strings for names).
#         - If 'roll_number' or 'name' is missing, ask the user for it.
#         - Provide the response in JSON format according to the schema below.
        
#         Schema:
#         {format_instructions}
        
#         Example:
#         User: "Add a new student named Jane Doe, roll number R100, in Computer Science department, with CGPA 8.5."
#         Output: {{"student_data": {{"name": "Jane Doe", "roll_number": "R100", "department": "Computer", "cgpa": 8.5}}}}
        
#         User: "Add Mike Smith from Data Science"
#         Output: {{"student_data": {{"name": "Mike Smith", "department": "Data Science"}}}} 
#         (Note: LLM should ideally ask for roll_number here if it's critical)

#         Request: {request}
#     """)
#     chain = prompt | get_llm() | parser

#     def _run(input_request: str):
#         try:
#             db_info = get_database_schema_info()
#             format_instructions = parser.get_format_instructions()
            
#             response = chain.invoke({
#                 "request": input_request,
#                 "sample_columns": db_info['sample_columns'],
#                 "format_instructions": format_instructions
#             })

#             student_data = response.get('student_data', {})
#             print(f"DEBUG: Parsed add student data: {student_data}")

#             if not student_data:
#                 return "I couldn't extract enough information to add a new student. Please provide more details like name and roll number."
            
#             if "name" not in student_data or "roll_number" not in student_data:
#                  return f"To add a new student, I need at least their name and roll number. Please provide both."
            
#             result = add_student(student_data)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return f"Error adding student: {result}. This might be due to a duplicate roll number or missing required fields."
            
#             return f"Successfully added student: {result.get('name', 'N/A')} (Roll No: {result.get('roll_number', 'N/A')})."
#         except Exception as e:
#             print(f"DEBUG: Exception in build_add_student_tool: {str(e)}")
#             return f"Error processing add student request: {str(e)}"
    
#     return Tool(
#         name="AddStudentToDatabase",
#         func=_run,
#         description=(
#             "Use this tool to add a new student record to the database. "
#             "Input should be a natural language request describing the new student, "
#             "e.g., 'Add a student named Alice, roll number R007, department Computer, CGPA 9.1'."
#             "Requires at least 'name' and 'roll_number'."
#         )
#     )

# def build_update_student_tool():
#     """Tool for updating existing student data."""
#     parser = JsonOutputParser(pydantic_object=UpdateStudentData)

#     prompt = PromptTemplate.from_template("""
#         You are an assistant that extracts filters and new data from natural language requests to update a student.
        
#         ACTUAL DATABASE INFO (if available):
#         - Sample columns: {sample_columns}
        
#         CRITICAL: 
#         - Identify clear filters (e.g., roll_number, email, or a combination like name and department) to pinpoint the student(s) to update.
#         - Extract the new values for the fields that need to be changed.
#         - If unique identification is ambiguous, ask for clarification (e.g., "Which John Doe?").
#         - Provide the response in JSON format according to the schema below.
        
#         Schema:
#         {format_instructions}
        
#         Example:
#         User: "Change Jane Doe's CGPA to 9.0"
#         Output: {{"filters": {{"name": "Jane Doe"}}, "new_data": {{"cgpa": 9.0}}}}
#         (Note: LLM should ideally ask for roll_number if multiple Jane Does exist)
        
#         User: "For student R001, update department to Data Science and internship status to completed."
#         Output: {{"filters": {{"roll_number": "R001"}}, "new_data": {{"department": "Data Science", "internship_status": "completed"}}}}
        
#         Request: {request}
#     """)
#     chain = prompt | get_llm() | parser

#     def _run(input_request: str):
#         try:
#             db_info = get_database_schema_info()
#             format_instructions = parser.get_format_instructions()

#             response = chain.invoke({
#                 "request": input_request,
#                 "sample_columns": db_info['sample_columns'],
#                 "format_instructions": format_instructions
#             })

#             filters = response.get('filters', {})
#             new_data = response.get('new_data', {})
#             print(f"DEBUG: Parsed update filters: {filters}, new_data: {new_data}")

#             if not filters or not new_data:
#                 return "I couldn't determine what student(s) to update or what data to change. Please specify both clearly (e.g., 'Update roll number R001's CGPA to 9.2')."
            
#             # Check for unique identifier in filters
#             if not ("roll_number" in filters or "email" in filters or ("name" in filters and "department" in filters)):
#                 return "To update a student, I need a unique identifier like 'roll_number' or 'email', or a combination like 'name' and 'department'."

#             result = update_student(filters, new_data)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return f"Error updating student: {result}. This might be due to ambiguous filters or invalid data."
            
#             if not result:
#                 return "No student found matching the criteria for update. Please check the student's details."
            
#             return f"Successfully updated {len(result)} student(s)."
#         except Exception as e:
#             print(f"DEBUG: Exception in build_update_student_tool: {str(e)}")
#             return f"Error processing update student request: {str(e)}"
    
#     return Tool(
#         name="UpdateStudentInDatabase",
#         func=_run,
#         description=(
#             "Use this tool to modify existing student records in the database. "
#             "Input should be a natural language request specifying which student(s) to update "
#             "(e.g., by roll number, name, or department) and what new values to set. "
#             "Example: 'Change CGPA to 9.0 for student R001'."
#             "Requires unique identification of the student(s) and new data."
#         )
#     )

# def build_delete_student_tool():
#     """Tool for deleting existing student data."""
#     parser = JsonOutputParser(pydantic_object=DeleteStudentData)

#     prompt = PromptTemplate.from_template("""
#         You are an assistant that extracts filters from natural language requests to delete a student.
        
#         CRITICAL: 
#         - Identify clear filters (e.g., roll_number, email, or a combination like name and department) to pinpoint the student(s) to delete.
#         - If unique identification is ambiguous, ask for clarification (e.g., "Which John Doe do you want to delete?").
#         - Provide the response in JSON format according to the schema below.
        
#         Schema:
#         {format_instructions}
        
#         Example:
#         User: "Delete student R001"
#         Output: {{"filters": {{"roll_number": "R001"}}}}
        
#         User: "Remove Jane Doe from Computer department"
#         Output: {{"filters": {{"name": "Jane Doe", "department": "Computer"}}}}
        
#         Request: {request}
#     """)
#     chain = prompt | get_llm() | parser

#     def _run(input_request: str):
#         try:
#             format_instructions = parser.get_format_instructions()
#             response = chain.invoke({
#                 "request": input_request,
#                 "format_instructions": format_instructions
#             })

#             filters = response.get('filters', {})
#             print(f"DEBUG: Parsed delete filters: {filters}")

#             if not filters:
#                 return "I couldn't determine which student(s) to delete. Please specify clearly (e.g., 'Delete student with roll number R001' or 'Delete Jane Doe from Computer Science')."
            
#             # Check for unique identifier in filters
#             if not ("roll_number" in filters or "email" in filters or ("name" in filters and "department" in filters)):
#                 return "To delete a student, I need a unique identifier like 'roll_number' or 'email', or a combination like 'name' and 'department'."

#             result = delete_student(filters)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return f"Error deleting student: {result}. This might be due to ambiguous filters."
            
#             if not result:
#                 return "No student found matching the criteria for deletion."
            
#             return f"Successfully deleted {len(result)} student(s)."
#         except Exception as e:
#             print(f"DEBUG: Exception in build_delete_student_tool: {str(e)}")
#             return f"Error processing delete student request: {str(e)}"
    
#     return Tool(
#         name="DeleteStudentFromDatabase",
#         func=_run,
#         description=(
#             "Use this tool to remove student records from the database. "
#             "Input should be a natural language request specifying which student(s) to delete "
#             "(e.g., by roll number, name, or email). "
#             "Example: 'Delete student with roll number R001'."
#             "Requires unique identification of the student(s)."
#         )
#     )

# def run_llm_query(user_query):
#     """
#     Main function to run the LLM agent with multiple tools for CRUD operations.
#     """
#     llm = get_llm()
    
#     # Define all available tools
#     tools = [
#         build_student_query_tool(),
#         build_add_student_tool(),
#         build_update_student_tool(),
#         build_delete_student_tool()
#     ]

#     # Initialize the agent
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # This agent type is good for tool selection
#         verbose=True, # Set to True to see agent's thought process
#         handle_parsing_errors=True,
#         max_iterations=5, # Allow more iterations for complex multi-step reasoning
#         early_stopping_method="generate"
#     )

#     try:
#         response = agent.invoke({"input": user_query})
#         return response["output"]
#     except Exception as e:
#         print(f"Error in run_llm_query: {str(e)}")
#         return f"Error running LLM query: {str(e)}"

# Fixed utils/llm.py - COMPLETELY REWRITTEN WITH PROPER LANGCHAIN USAGE
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