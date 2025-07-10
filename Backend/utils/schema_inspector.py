# import logging
# import json
# import os
# import time
# from typing import Dict, Any, List, Union
# from abc import ABC, abstractmethod
# import redis

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class SchemaInspector:
#     """
#     Universal Schema Inspector that works with any database adapter.
#     Discovers tables/collections, column information, sample data, and relationships.
#     Caches schema information for performance.
#     """
    
#     # Cache duration in seconds (1 hour)
#     SCHEMA_CACHE_DURATION = 3600 

#     def __init__(self, db_adapter: Any):
#         """
#         Initializes the SchemaInspector with a database adapter.

#         Args:
#             db_adapter (Any): An instance of a database adapter (e.g., SupabaseAdapter, PostgreSQLAdapter).
#                               It must implement the methods defined in BaseAdapter.
#         """
#         self.db_adapter = db_adapter
#         self.schema_cache: Dict[str, Any] = {}
#         self.cache_key = f"schema:{hash(self.db_adapter.__class__.__name__)}" # Unique key per adapter type
#         self.redis_client = self._init_redis_client()

#     def _init_redis_client(self) -> Union[redis.Redis, None]:
#         """Initializes and returns a Redis client for caching, if REDIS_URL is set."""
#         redis_url = os.getenv("REDIS_URL")
#         if redis_url:
#             try:
#                 client = redis.from_url(redis_url, decode_responses=True)
#                 client.ping() # Test connection
#                 logging.info("Redis client initialized successfully for schema caching.")
#                 return client
#             except redis.exceptions.ConnectionError as e:
#                 logging.warning(f"Could not connect to Redis at {redis_url}. Schema caching will be in-memory only. Error: {e}")
#                 return None
#             except Exception as e:
#                 logging.warning(f"Unexpected error initializing Redis: {e}. Schema caching will be in-memory only.")
#                 return None
#         logging.info("REDIS_URL not set. Schema caching will be in-memory only.")
#         return None

#     def discover_schema(self) -> Dict[str, Any]:
#         """
#         Main method to discover the database schema.
#         Tries to load from cache first, otherwise performs live discovery.

#         Returns:
#             Dict[str, Any]: A dictionary representing the discovered schema.
#                             Format: {'tables': {'table_name': {'columns': [...], 'sample_data': [...], 'relationships': [...]}}}
#         """
#         cached_schema = self._load_schema_from_cache()
#         if cached_schema:
#             logging.info("Loaded schema from cache.")
#             self.schema_cache = cached_schema
#             return cached_schema

#         logging.info("Performing live schema discovery...")
#         schema = {'tables': {}}
#         try:
#             table_names = self.db_adapter.get_table_names()
#             if not table_names:
#                 logging.warning("No tables/collections found in the database.")
#                 return schema

#             for table_name in table_names:
#                 logging.info(f"Discovering schema for table/collection: {table_name}")
#                 table_info = {
#                     'columns': self.db_adapter.get_column_info(table_name),
#                     'sample_data': self.db_adapter.get_sample_records(table_name, limit=3),
#                     'relationships': self.db_adapter.detect_relationships(table_name)
#                 }
#                 schema['tables'][table_name] = table_info
                
#             self._cache_schema(schema)
#             logging.info("Live schema discovery complete and cached.")
#             return schema
#         except Exception as e:
#             logging.error(f"Error during schema discovery: {e}", exc_info=True)
#             raise ValueError(f"Failed to discover database schema: {str(e)}")

#     def _load_schema_from_cache(self) -> Union[Dict[str, Any], None]:
#         """
#         Loads schema from Redis cache if available and not expired.
#         Falls back to in-memory cache if Redis is not configured or fails.
#         """
#         if self.redis_client:
#             try:
#                 cached_data = self.redis_client.get(self.cache_key)
#                 if cached_data:
#                     cached_schema = json.loads(cached_data)
#                     logging.info(f"Schema found in Redis cache for key: {self.cache_key}")
#                     return cached_schema
#             except Exception as e:
#                 logging.warning(f"Error loading schema from Redis: {e}. Falling back to in-memory cache.")
        
#         # Fallback to in-memory cache
#         if self.schema_cache and (time.time() - self.schema_cache.get('timestamp', 0) < self.SCHEMA_CACHE_DURATION):
#             logging.info("Schema found in in-memory cache.")
#             return self.schema_cache['data']
        
#         return None

#     def _cache_schema(self, schema: Dict[str, Any]) -> None:
#         """
#         Caches the discovered schema, first to Redis if available, then to in-memory.
#         """
#         schema_with_timestamp = {'data': schema, 'timestamp': time.time()}
        
#         if self.redis_client:
#             try:
#                 self.redis_client.setex(self.cache_key, self.SCHEMA_CACHE_DURATION, json.dumps(schema_with_timestamp['data']))
#                 logging.info(f"Schema cached to Redis for key: {self.cache_key}")
#             except Exception as e:
#                 logging.warning(f"Error caching schema to Redis: {e}. Caching to in-memory only.")
        
#         self.schema_cache = schema_with_timestamp
#         logging.info("Schema cached to in-memory.")

#     def get_tables(self) -> List[str]:
#         """
#         Returns a list of all table/collection names from the cached schema.

#         Returns:
#             List[str]: A list of table/collection names.
#         """
#         if not self.schema_cache:
#             self.discover_schema() # Ensure schema is loaded
#         return list(self.schema_cache.get('data', {}).get('tables', {}).keys())

#     def get_columns(self, table: str) -> List[Dict[str, str]]:
#         """
#         Returns column information for a specific table from the cached schema.

#         Args:
#             table (str): The name of the table/collection.

#         Returns:
#             List[Dict[str, str]]: A list of dictionaries, each representing a column.
#                                    Format: [{'name': 'column_name', 'type': 'data_type'}]
#         """
#         if not self.schema_cache:
#             self.discover_schema()
#         return self.schema_cache.get('data', {}).get('tables', {}).get(table, {}).get('columns', [])

#     def get_sample_data(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
#         """
#         Returns sample data for a specific table from the cached schema.

#         Args:
#             table (str): The name of the table/collection.
#             limit (int): The maximum number of sample records to return.

#         Returns:
#             List[Dict[str, Any]]: A list of dictionaries, each representing a sample record.
#         """
#         if not self.schema_cache:
#             self.discover_schema()
#         # The sample data is already limited during discovery, so just return what's cached
#         return self.schema_cache.get('data', {}).get('tables', {}).get(table, {}).get('sample_data', [])[:limit]

#     def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
#         """
#         Returns detected relationships for a specific table from the cached schema.

#         Args:
#             table (str): The name of the table/collection.

#         Returns:
#             List[Dict[str, Any]]: A list of dictionaries, each representing a relationship.
#         """
#         if not self.schema_cache:
#             self.discover_schema()
#         return self.schema_cache.get('data', {}).get('tables', {}).get(table, {}).get('relationships', [])