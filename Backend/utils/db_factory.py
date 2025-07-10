# import os
# import logging
# from typing import Dict, Any, Tuple, Union
# from dotenv import load_dotenv

# from utils.adapters.supabase_adapter import SupabaseAdapter
# from utils.adapters.firebase_adapter import FirebaseAdapter
# from utils.adapters.mongodb_adapter import MongoDBAdapter
# from utils.adapters.postgresql_adapter import PostgreSQLAdapter
# from utils.schema_inspector import SchemaInspector

# load_dotenv()
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class DatabaseFactory:
#     """
#     Factory class to detect database type, instantiate appropriate adapter,
#     test connection, and auto-discover schema.
#     """

#     @staticmethod
#     def create_connection(connection_config: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
#         """
#         Main factory method to create a database connection, test it, and discover its schema.

#         Args:
#             connection_config (Dict[str, Any]): Dictionary containing connection parameters.
#                                                  Must include 'type' (e.g., 'supabase', 'firebase', 'mongodb', 'postgresql')
#                                                  and other type-specific parameters.

#         Returns:
#             Tuple[Any, Dict[str, Any]]: A tuple containing the instantiated database adapter
#                                         and the discovered schema.

#         Raises:
#             ValueError: If the connection configuration is invalid or connection fails.
#             Exception: For other unexpected errors during connection or schema discovery.
#         """
#         db_type = DatabaseFactory.detect_database_type(connection_config)
#         DatabaseFactory.validate_config(connection_config, db_type)

#         adapter = None
#         try:
#             if db_type == 'supabase':
#                 url = connection_config.get('url', os.getenv("SUPABASE_URL"))
#                 key = connection_config.get('key', os.getenv("SUPABASE_KEY"))
#                 if not url or not key:
#                     raise ValueError("Supabase URL and Key must be provided in config or .env")
#                 adapter = SupabaseAdapter(url, key)
#             elif db_type == 'firebase':
#                 credentials_path = connection_config.get('credentials_path', os.getenv("FIREBASE_CREDENTIALS_PATH"))
#                 if not credentials_path:
#                     raise ValueError("Firebase credentials path must be provided in config or .env")
#                 adapter = FirebaseAdapter(credentials_path)
#             elif db_type == 'mongodb':
#                 connection_string = connection_config.get('connection_string', os.getenv("MONGO_DB_CONNECTION_STRING"))
#                 database_name = connection_config.get('database_name')
#                 if not connection_string or not database_name:
#                     raise ValueError("MongoDB connection string and database name must be provided in config or .env")
#                 adapter = MongoDBAdapter(connection_string, database_name)
#             elif db_type == 'postgresql':
#                 connection_string = connection_config.get('connection_string', os.getenv("POSTGRES_CONNECTION_STRING"))
#                 if not connection_string:
#                     raise ValueError("PostgreSQL connection string must be provided in config or .env")
#                 adapter = PostgreSQLAdapter(connection_string)
#             else:
#                 raise ValueError(f"Unsupported database type: {db_type}")

#             if not adapter.test_connection():
#                 raise ValueError(f"Failed to establish connection to {db_type} database.")
#             logging.info(f"Successfully connected to {db_type} database.")

#             # Auto-discover schema
#             schema_inspector = SchemaInspector(adapter)
#             discovered_schema = schema_inspector.discover_schema()
#             logging.info(f"Successfully discovered schema for {db_type} database.")

#             return adapter, discovered_schema

#         except ValueError as e:
#             logging.error(f"Configuration or connection error for {db_type}: {e}")
#             if adapter and hasattr(adapter, 'close'):
#                 adapter.close()
#             raise
#         except Exception as e:
#             logging.error(f"An unexpected error occurred during database connection for {db_type}: {e}", exc_info=True)
#             if adapter and hasattr(adapter, 'close'):
#                 adapter.close()
#             raise ValueError(f"An unexpected error occurred: {str(e)}")


#     @staticmethod
#     def detect_database_type(config: Dict[str, Any]) -> str:
#         """
#         Auto-detects the database type from the connection configuration.

#         Args:
#             config (Dict[str, Any]): The connection configuration dictionary.

#         Returns:
#             str: The detected database type (e.g., 'supabase', 'firebase', 'mongodb', 'postgresql').

#         Raises:
#             ValueError: If the database type cannot be determined.
#         """
#         db_type = config.get('type')
#         if db_type and isinstance(db_type, str):
#             db_type_lower = db_type.lower()
#             if db_type_lower in ['supabase', 'firebase', 'mongodb', 'postgresql']:
#                 return db_type_lower
#             else:
#                 raise ValueError(f"Unknown database type specified: {db_type}. Supported types are 'supabase', 'firebase', 'mongodb', 'postgresql'.")
        
#         # Attempt to infer from keys if 'type' is missing
#         if any(k in config for k in ['url', 'key', 'supabase_url', 'supabase_key']):
#             logging.info("Inferred Supabase type from config keys.")
#             return 'supabase'
#         if 'credentials_path' in config or 'firebase_credentials' in config:
#             logging.info("Inferred Firebase type from config keys.")
#             return 'firebase'
#         if 'connection_string' in config and 'mongodb' in config['connection_string'].lower():
#             logging.info("Inferred MongoDB type from connection string.")
#             return 'mongodb'
#         if 'connection_string' in config and 'postgresql' in config['connection_string'].lower():
#             logging.info("Inferred PostgreSQL type from connection string.")
#             return 'postgresql'

#         raise ValueError("Could not detect database type. Please specify 'type' in connection_config or provide standard connection keys.")

#     @staticmethod
#     def validate_config(config: Dict[str, Any], db_type: str) -> None:
#         """
#         Validates the configuration based on the detected database type.

#         Args:
#             config (Dict[str, Any]): The connection configuration dictionary.
#             db_type (str): The detected database type.

#         Raises:
#             ValueError: If the configuration is missing required parameters for the given database type.
#         """
#         if db_type == 'supabase':
#             if not (config.get('url') or os.getenv("SUPABASE_URL")) or \
#                not (config.get('key') or os.getenv("SUPABASE_KEY")):
#                 raise ValueError("Supabase connection requires 'url' and 'key'.")
#         elif db_type == 'firebase':
#             if not (config.get('credentials_path') or os.getenv("FIREBASE_CREDENTIALS_PATH")):
#                 raise ValueError("Firebase connection requires 'credentials_path'.")
#             if not os.path.exists(config.get('credentials_path', os.getenv("FIREBASE_CREDENTIALS_PATH"))):
#                 raise ValueError(f"Firebase credentials file not found at: {config.get('credentials_path', os.getenv('FIREBASE_CREDENTIALS_PATH'))}")
#         elif db_type == 'mongodb':
#             if not (config.get('connection_string') or os.getenv("MONGO_DB_CONNECTION_STRING")):
#                 raise ValueError("MongoDB connection requires 'connection_string'.")
#             if not config.get('database_name'):
#                 raise ValueError("MongoDB connection requires 'database_name'.")
#         elif db_type == 'postgresql':
#             if not (config.get('connection_string') or os.getenv("POSTGRES_CONNECTION_STRING")):
#                 raise ValueError("PostgreSQL connection requires 'connection_string'.")
#         else:
#             raise ValueError(f"Validation not implemented for unknown database type: {db_type}")