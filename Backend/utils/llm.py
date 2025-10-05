# import os
# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from typing import List, Dict, Union, Any

# # Import database interaction functions
# from utils.db import (
#     dynamic_student_query, get_students,
#     add_student, update_student, delete_student
# )

# # ... (QueryClassifier, get_database_schema_info, get_llm, clean_json_output functions remain the same) ...

# class QueryClassifier:
#     """Classifies user queries into CRUD operations"""
    
#     def __init__(self, llm):
#         self.llm = llm
    
#     def classify_query(self, query: str) -> str:
#         """Classify the query into one of: query, add, update, delete"""
#         prompt = f"""
#         Classify the following user query into one of these categories:
#         - "query": For searching, finding, listing, or retrieving student information
#         - "add": For adding, creating, or inserting new student records
#         - "update": For modifying, changing, or updating existing student information
#         - "delete": For removing, deleting, or eliminating student records
        
#         User query: "{query}"
        
#         Return only one word: query, add, update, or delete
#         """
        
#         try:
#             response = self.llm.invoke([HumanMessage(content=prompt)])
#             classification = response.content.strip().lower()
            
#             if classification in ['query', 'add', 'update', 'delete']:
#                 return classification
#             else:
#                 return 'query'  # Default to query if unclear
#         except Exception as e:
#             print(f"Error in classify_query: {e}")
#             return 'query'

# def get_database_schema_info():
#     """
#     Fetches basic schema information from the database to help the LLM.
#     """
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
#         return {'departments': [], 'sample_columns': [], 'total_count': 0}
#     except Exception as e:
#         print(f"ERROR: Error getting database schema info: {e}")
#         return {'departments': [], 'sample_columns': [], 'total_count': 0}

# def get_llm():
#     """Returns a configured ChatGoogleGenerativeAI instance."""
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("GEMINI_API_KEY must be set in environment variables")
    
#     return ChatGoogleGenerativeAI(
#         model="gemini-2.0-flash-exp",
#         google_api_key=api_key,
#         temperature=0.1
#     )

# def clean_json_output(text: str) -> str:
#     """Clean JSON output from LLM response"""
#     # Remove markdown code blocks
#     text = re.sub(r'```json\s*', '', text)
#     text = re.sub(r'```\s*$', '', text)
#     text = text.strip()
    
#     # Find JSON object in the text
#     json_match = re.search(r'\{.*\}', text, re.DOTALL)
#     if json_match:
#         return json_match.group(0)
    
#     return text

# def handle_query_operation(user_query: str, llm) -> str:
#     """Handle database query operations with a single LLM call."""
#     try:
#         db_info = get_database_schema_info()
        
#         prompt = f"""
#         Extract database filter conditions from this student query.
        
#         Available departments: {db_info['departments']}
#         Available columns: {db_info['sample_columns']}
        
#         IMPORTANT: Use exact department names from the list above.
#         Map common terms: "cs" -> "Computer", "mech" -> "Mechanical", etc.
        
#         Common column mappings:
#         - "gpa", "cgpa" -> "cgpa"
#         - "name" -> "name"
#         - "roll number" -> "roll_number"
        
#         Operators: eq, gt, lt, gte, lte, like
        
#         Query: "{user_query}"
        
#         Return JSON format: {{"filters": {{"column_name": {{"op": "operator", "value": "value"}}}}}}
#         If no filters, return: {{"filters": {{}}}}
#         """
        
#         response = llm.invoke([HumanMessage(content=prompt)])
#         cleaned_response = clean_json_output(response.content)
        
#         try:
#             parsed = json.loads(cleaned_response)
#             filters = parsed.get('filters', {})
            
#             result = get_students() if not filters else dynamic_student_query(filters)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return json.dumps({"error": result})
            
#             if not result:
#                 return json.dumps({"message": "No students found matching your criteria."})
            
#             # Limit the data sent to the frontend
#             if len(result) > 5:
#                 message = f"Found {len(result)} students. Showing the first 5."
#                 return json.dumps({"message": message, "students": result[:5]})
#             else:
#                 message = f"Found {len(result)} student(s)."
#                 return json.dumps({"message": message, "students": result})
                
#         except json.JSONDecodeError as e:
#             return json.dumps({"error": f"Error parsing query filters: {e}. Raw response: {cleaned_response}"})
            
#     except Exception as e:
#         return json.dumps({"error": f"Error processing query: {str(e)}"})

# # ... (handle_add_operation, handle_update_operation, handle_delete_operation remain the same as the previous step) ...
# # ... (run_llm_query remains the same as the previous step) ...
# def handle_add_operation(user_query: str, llm) -> str:
#     """Handle add student operations"""
#     try:
#         prompt = f"""
#         Extract student data from this request to add a new student.
        
#         Request: "{user_query}"
        
#         Return JSON format:
#         {{"student_data": {{"name": "value", "roll_number": "value", "department": "value", "cgpa": 0.0}}}}
        
#         Include all available information. At minimum need name and roll_number.
#         If insufficient info, return: {{"student_data": {{}}}}
#         """
        
#         response = llm.invoke([HumanMessage(content=prompt)])
#         cleaned_response = clean_json_output(response.content)
        
#         try:
#             parsed = json.loads(cleaned_response)
#             student_data = parsed.get('student_data', {})
            
#             if not student_data or 'name' not in student_data or 'roll_number' not in student_data:
#                 return json.dumps({"error": "To add a student, I need at least their name and roll number. Please provide both."})
            
#             result = add_student(student_data)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return json.dumps({"error": result})
            
#             return json.dumps({"message": f"Successfully added student: {result.get('name', 'N/A')} (Roll No: {result.get('roll_number', 'N/A')})"})
            
#         except json.JSONDecodeError as e:
#             return json.dumps({"error": f"Error parsing add data: {e}. Raw response: {cleaned_response}"})
            
#     except Exception as e:
#         return json.dumps({"error": f"Error processing add request: {str(e)}"})

# def handle_update_operation(user_query: str, llm) -> str:
#     """Handle update student operations"""
#     try:
#         prompt = f"""
#         Extract filters and new data from this update request.
        
#         Request: "{user_query}"
        
#         Return JSON format:
#         {{"filters": {{"roll_number": "value"}}, "new_data": {{"column": "new_value"}}}}
        
#         Use roll_number or email for unique identification.
#         If unclear, return: {{"filters": {{}}, "new_data": {{}}}}
#         """
        
#         response = llm.invoke([HumanMessage(content=prompt)])
#         cleaned_response = clean_json_output(response.content)
        
#         try:
#             parsed = json.loads(cleaned_response)
#             filters = parsed.get('filters', {})
#             new_data = parsed.get('new_data', {})
            
#             if not filters or not new_data:
#                 return json.dumps({"error": "Please specify both which student to update and what data to change."})
            
#             result = update_student(filters, new_data)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return json.dumps({"error": result})
            
#             if not result:
#                 return json.dumps({"message": "No student found matching the criteria for update."})
            
#             return json.dumps({"message": f"Successfully updated {len(result)} student(s)."})
            
#         except json.JSONDecodeError as e:
#             return json.dumps({"error": f"Error parsing update data: {e}. Raw response: {cleaned_response}"})
            
#     except Exception as e:
#         return json.dumps({"error": f"Error processing update request: {str(e)}"})

# def handle_delete_operation(user_query: str, llm) -> str:
#     """Handle delete student operations"""
#     try:
#         prompt = f"""
#         Extract filters from this delete request.
        
#         Request: "{user_query}"
        
#         Return JSON format:
#         {{"filters": {{"roll_number": "value"}}}}
        
#         Use roll_number or email for unique identification.
#         If unclear, return: {{"filters": {{}}}}
#         """
        
#         response = llm.invoke([HumanMessage(content=prompt)])
#         cleaned_response = clean_json_output(response.content)
        
#         try:
#             parsed = json.loads(cleaned_response)
#             filters = parsed.get('filters', {})
            
#             if not filters:
#                 return json.dumps({"error": "Please specify which student to delete using roll number or email."})
            
#             result = delete_student(filters)
            
#             if isinstance(result, str) and result.startswith("Error"):
#                 return json.dumps({"error": result})
            
#             if not result:
#                 return json.dumps({"message": "No student found matching the criteria for deletion."})
            
#             return json.dumps({"message": f"Successfully deleted {len(result)} student(s)."})
            
#         except json.JSONDecodeError as e:
#             return json.dumps({"error": f"Error parsing delete filters: {e}. Raw response: {cleaned_response}"})
            
#     except Exception as e:
#         return json.dumps({"error": f"Error processing delete request: {str(e)}"})

# def run_llm_query(user_query: str) -> str:
#     """
#     Main function to process user queries using LLM without complex agents
#     """
#     greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
#     if user_query.lower().strip() in greetings:
#         return json.dumps({"message": "Hello! How can I help you with the student database today?"})

#     try:
#         llm = get_llm()
#         classifier = QueryClassifier(llm)
        
#         operation = classifier.classify_query(user_query)
#         print(f"DEBUG: Classified operation: {operation}")
        
#         if operation == 'add':
#             return handle_add_operation(user_query, llm)
#         elif operation == 'update':
#             return handle_update_operation(user_query, llm)
#         elif operation == 'delete':
#             return handle_delete_operation(user_query, llm)
#         else:
#             return handle_query_operation(user_query, llm)
            
#     except Exception as e:
#         print(f"Error in run_llm_query: {str(e)}")
#         return json.dumps({"error": f"Error processing your request: {str(e)}. Please try again or rephrase your query."})

import os
import traceback
from dotenv import load_dotenv

from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from pymongo import MongoClient

# Corrected imports for MongoDB using the correct class name
from langchain_mongodb.agent_toolkit import MongoDBDatabaseToolkit
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables from .env file
load_dotenv()

def get_llm(use_vertex=False):
    """Returns a configured LLM instance, switching between standard and Vertex AI."""
    if use_vertex:
        return ChatVertexAI(
            model_name="gemini-1.5-flash-001",
            temperature=0,
            project=os.getenv("GOOGLE_CLOUD_PROJECT")
        )
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY must be set in environment variables or .env file")
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0,
            convert_system_message_to_human=True
        )

def run_llm_query(user_query: str, db_uri: str, db_type: str, mode: str, session) -> dict:
    """Processes a user's query by routing it to the appropriate agent."""
    try:
        llm = get_llm(use_vertex=False)
        agent_executor = None

        if db_type in ['postgresql', 'mysql']:
            # Create SQL Database connection
            db = SQLDatabase.from_uri(db_uri)
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)
            
            # Custom prompt suffix based on mode
            custom_prompt_suffix = ""
            if mode == 'read-only':
                custom_prompt_suffix = (
                    "\n\nIMPORTANT CONSTRAINTS:\n"
                    "- You are in READ-ONLY MODE\n"
                    "- You MUST NOT execute any INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE statements\n"
                    "- Only SELECT queries are permitted\n"
                    "- If the user asks to modify data, politely inform them that you're in read-only mode\n"
                )
            else:
                custom_prompt_suffix = (
                    "\n\nIMPORTANT:\n"
                    "- You are in READ-WRITE MODE\n"
                    "- You can execute INSERT, UPDATE, DELETE queries when requested\n"
                    "- Always confirm the action before executing destructive operations\n"
                    "- Be cautious with UPDATE and DELETE queries - always use WHERE clauses appropriately\n"
                )
            
            # Create SQL agent with enhanced configuration
            agent_executor = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=True,
                agent_type="openai-tools",
                suffix=custom_prompt_suffix,
                max_iterations=10,
                max_execution_time=30,
                early_stopping_method="generate"
            )

        elif db_type == 'mongodb':
            # Create MongoDB connection
            client = MongoClient(db_uri, serverSelectionTimeoutMS=5000)
            
            # Extract database name from URI
            db_name = db_uri.split('/')[-1].split('?')[0]
            if not db_name or db_name == '':
                # Default to 'test' if no database specified
                db_name = 'test'
            
            db = client[db_name]

            # Create MongoDB toolkit
            toolkit = MongoDBDatabaseToolkit(db=db, llm=llm)
            tools = toolkit.get_tools()

            # System prompt with mode-specific instructions
            if mode == 'read-only':
                system_prompt = (
                    "You are a helpful AI assistant for querying a MongoDB database. "
                    "You have access to tools to interact with the database. "
                    "IMPORTANT: You are in READ-ONLY MODE. "
                    "You can only perform read operations (find, aggregate, count). "
                    "You MUST NOT perform any write operations (insert, update, delete). "
                    "If the user asks to modify data, politely inform them that you're in read-only mode. "
                    "Given a user's question, decide which tool to use and provide a clear answer."
                )
            else:
                system_prompt = (
                    "You are a helpful AI assistant for querying and managing a MongoDB database. "
                    "You have access to tools to interact with the database. "
                    "You are in READ-WRITE MODE and can perform both read and write operations. "
                    "Be cautious with write operations and confirm the action before executing. "
                    "Given a user's question, decide which tool to use and provide a clear answer."
                )
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])

            # Create agent and executor
            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent, 
                tools=tools, 
                verbose=True,
                max_iterations=10,
                max_execution_time=30,
                early_stopping_method="generate"
            )

        if not agent_executor:
            return {'error': f"Agent for database type '{db_type}' is not implemented."}

        # Execute the query
        response = agent_executor.invoke({
            "input": user_query,
            "chat_history": []  # Can be extended to include conversation history
        })
        
        final_answer = response.get('output', 'No answer found.')
        
        # Log to history if in read-write mode and a write operation was performed
        # (This is a simplified version - in production, you'd detect actual write operations)
        if mode == 'read-write' and any(keyword in user_query.lower() for keyword in ['insert', 'update', 'delete', 'create', 'drop', 'alter']):
            if 'history' not in session:
                session['history'] = []
            
            session['history'].append({
                'query': user_query,
                'description': f"Executed: {user_query[:100]}...",
                'timestamp': str(os.times()),
                'reverted': False
            })
            session.modified = True
        
        return {'response': final_answer}

    except Exception as e:
        print(f"Error in run_llm_query: {traceback.format_exc()}")
        return {'error': f"The AI agent encountered an error: {str(e)}. Please check your connection and query."}