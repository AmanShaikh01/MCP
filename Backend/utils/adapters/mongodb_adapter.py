import logging
from typing import List, Dict, Any, Union
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from utils.adapters.__init__ import BaseAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MongoDBAdapter(BaseAdapter):
    """
    MongoDB Atlas adapter for the universal query system.
    Handles MongoDB connections, schema introspection (dynamic document schema),
    and query execution for collections.
    """

    def __init__(self, connection_string: str, database_name: str):
        """
        Initializes the MongoDBAdapter.

        Args:
            connection_string (str): The MongoDB connection string (e.g., "mongodb+srv://user:pass@cluster.mongodb.net/").
            database_name (str): The name of the database to connect to.
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: MongoClient = None
        self.db: Any = None # pymongo.database.Database
        self._initialize_client()

    def _initialize_client(self):
        """Initializes the MongoDB client and selects the database."""
        try:
            # Use serverSelectionTimeoutMS to prevent indefinite hanging
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # The actual connection isn't made until an operation is attempted,
            # but this preps the client.
            self.db = self.client[self.database_name]
            logging.info(f"MongoDB client initialized for database: {self.database_name}")
        except Exception as e:
            logging.error(f"Failed to initialize MongoDB client: {e}", exc_info=True)
            raise ConnectionError(f"MongoDB initialization failed: {e}")

    def test_connection(self) -> bool:
        """
        Tests the MongoDB connection by attempting a simple database command (e.g., list collection names).
        """
        try:
            # The 'list_collection_names' forces a connection
            collection_names = self.db.list_collection_names()
            logging.info(f"MongoDB connection test successful. Found collections: {collection_names}")
            return True
        except ConnectionFailure as e:
            logging.error(f"MongoDB connection test failed - ConnectionFailure: {e}", exc_info=True)
            return False
        except OperationFailure as e:
            logging.error(f"MongoDB connection test failed - OperationFailure (auth/permissions?): {e}", exc_info=True)
            return False
        except PyMongoError as e:
            logging.error(f"MongoDB connection test failed - PyMongoError: {e}", exc_info=True)
            return False
        except Exception as e:
            logging.error(f"MongoDB connection test failed - Unexpected error: {e}", exc_info=True)
            return False

    def get_table_names(self) -> List[str]:
        """
        Retrieves all collection names within the connected MongoDB database.
        """
        try:
            collection_names = self.db.list_collection_names()
            logging.info(f"MongoDB discovered collections: {collection_names}")
            return collection_names
        except Exception as e:
            logging.error(f"Error getting MongoDB collection names: {e}", exc_info=True)
            return []

    def get_column_info(self, table: str) -> List[Dict[str, str]]:
        """
        Infers 'column' (field) information for a MongoDB collection by inspecting sample documents.
        MongoDB is schemaless, so this is an inference based on actual data.
        """
        columns_info = []
        try:
            # Get a few sample documents to infer schema
            sample_docs = self.get_sample_records(table, limit=5)
            
            seen_fields = set()
            for doc in sample_docs:
                for field_name, field_value in doc.items():
                    if field_name not in seen_fields and field_name != '_id': # Exclude default MongoDB _id
                        # Infer type (basic inference)
                        field_type = type(field_value).__name__
                        if isinstance(field_value, dict):
                            field_type = 'object'
                        elif isinstance(field_value, list):
                            field_type = 'array'
                        elif isinstance(field_value, int):
                            field_type = 'integer'
                        elif isinstance(field_value, float):
                            field_type = 'double'
                        elif isinstance(field_value, bool):
                            field_type = 'boolean'
                        elif isinstance(field_value, str):
                            field_type = 'string'
                        # Add more types as needed (e.g., datetime, ObjectId)

                        columns_info.append({'name': field_name, 'type': field_type})
                        seen_fields.add(field_name)
            
            logging.info(f"MongoDB inferred columns for {table}: {columns_info}")
            return columns_info
        except Exception as e:
            logging.error(f"Error inferring MongoDB column info for {table}: {e}", exc_info=True)
            return []

    def execute_query(self, query_params: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a MongoDB query based on the provided parameters.
        """
        table = query_params.get('table')
        # columns = query_params.get('columns', ['*']) # Not directly applicable for selection in MongoDB find() without projection
        filters = query_params.get('filters', {})
        limit = query_params.get('limit', 100)

        if not table:
            return "Error: Collection name not provided for MongoDB query execution."

        try:
            collection = self.db[table]
            
            mongo_filters = {}
            for field_name, condition in filters.items():
                op = condition.get('op')
                value = condition.get('value')

                if op == 'eq':
                    mongo_filters[field_name] = value
                elif op == 'gt':
                    mongo_filters[field_name] = {'$gt': value}
                elif op == 'lt':
                    mongo_filters[field_name] = {'$lt': value}
                elif op == 'gte':
                    mongo_filters[field_name] = {'$gte': value}
                elif op == 'lte':
                    mongo_filters[field_name] = {'$lte': value}
                elif op == 'like':
                    # MongoDB regex for 'like' (case-insensitive example)
                    # Note: Using regex on unindexed fields can be slow.
                    mongo_filters[field_name] = {'$regex': value, '$options': 'i'} # 'i' for case-insensitive
                elif op == 'ilike': # Alias for case-insensitive like
                    mongo_filters[field_name] = {'$regex': value, '$options': 'i'}
                elif op == 'in':
                    if isinstance(value, list):
                        mongo_filters[field_name] = {'$in': value}
                    else:
                        logging.warning(f"MongoDB 'in' operator expects a list, got {type(value)} for {field_name}. Skipping filter.")
                elif op == 'nin':
                    if isinstance(value, list):
                        mongo_filters[field_name] = {'$nin': value}
                    else:
                        logging.warning(f"MongoDB 'nin' operator expects a list, got {type(value)} for {field_name}. Skipping filter.")
                else:
                    logging.warning(f"Unsupported operator '{op}' for MongoDB for field '{field_name}'. Skipping filter.")
                    return f"Error: Unsupported operator '{op}' for MongoDB for field '{field_name}'."
            
            # For select queries, if specific columns are requested, we'd add a projection.
            # `columns` in query_params would be passed to `find({}, projection_dict)`
            # For simplicity, returning all fields for now.
            
            cursor = collection.find(mongo_filters).limit(limit)
            results = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in results:
                if '_id' in doc:
                    doc['id'] = str(doc['_id'])
                    del doc['_id'] # Remove original _id field

            logging.info(f"MongoDB query executed successfully for '{table}'. Results: {len(results)}")
            return results
        except PyMongoError as pe:
            error_msg = f"MongoDB operation error executing query for collection '{table}': {pe}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        except Exception as e:
            error_msg = f"Error executing MongoDB query for collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def build_select_query(self, table: str, columns: List[str], filters: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """
        Builds a dictionary representing a MongoDB find query.
        """
        return {
            'table': table,
            'columns': columns, # These can be used for projection later if needed
            'filters': filters,
            'limit': limit
        }

    def get_sample_records(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves sample documents from a MongoDB collection.
        """
        try:
            collection = self.db[table]
            cursor = collection.find({}).limit(limit)
            sample_data = list(cursor)
            
            # Convert ObjectId to string for JSON serialization
            for doc in sample_data:
                if '_id' in doc:
                    doc['id'] = str(doc['_id'])
                    del doc['_id']

            logging.info(f"MongoDB fetched {len(sample_data)} sample records from {table}.")
            return sample_data
        except PyMongoError as pe:
            logging.error(f"Error getting MongoDB sample records for {table}: {pe}", exc_info=True)
            return []
        except Exception as e:
            logging.error(f"Error getting MongoDB sample records for {table}: {e}", exc_info=True)
            return []
    
    def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
        """
        Detects relationships in MongoDB. This is highly application-specific
        due to MongoDB's schemaless nature. Relationships are typically
        embedded or referenced by IDs. For Phase 1, we will return an empty list.
        Advanced versions could try to infer from field names like 'foreignTableId'.
        """
        logging.info(f"MongoDB does not have explicit foreign key relationships like relational databases. Relationships for '{table}' need to be inferred from application logic. Returning empty list for now.")
        return []

    def add_record(self, table: str, data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """Adds a new document to a MongoDB collection."""
        try:
            collection = self.db[table]
            # If 'id' is provided, we can map it to '_id' for MongoDB.
            if 'id' in data:
                data['_id'] = data.pop('id')

            result = collection.insert_one(data)
            
            inserted_id = str(result.inserted_id) # Convert ObjectId to string
            inserted_data = data.copy()
            inserted_data['id'] = inserted_id
            if '_id' in inserted_data: # Clean up the original _id if it was present
                del inserted_data['_id']
            logging.info(f"Added record to MongoDB collection '{table}' with ID: {inserted_id}")
            return inserted_data
        except PyMongoError as pe:
            error_msg = f"Error adding record to MongoDB collection '{table}': {pe}"
            logging.error(error_msg, exc_info=True)
            # Check for duplicate key errors for unique indexes
            if pe.code == 11000: # Duplicate key error code
                return f"Error: A record with a conflicting unique key already exists in '{table}'."
            return error_msg
        except Exception as e:
            error_msg = f"Error adding record to MongoDB collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def update_record(self, table: str, filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Updates records in a MongoDB collection based on filters."""
        try:
            collection = self.db[table]
            mongo_filters = {}
            for field_name, condition in filters.items():
                op = condition.get('op')
                value = condition.get('value')

                # Special handling for 'id' which maps to '_id' in MongoDB
                if field_name == 'id':
                    from bson.objectid import ObjectId
                    if isinstance(value, str):
                        try:
                            value = ObjectId(value)
                        except:
                            logging.warning(f"Invalid ObjectId string for 'id' filter: {value}. Proceeding as string match.")
                    field_name = '_id'

                if op == 'eq':
                    mongo_filters[field_name] = value
                else:
                    logging.warning(f"MongoDB update filter only supports 'eq' for now. Skipping filter '{field_name}' with op '{op}'.")
                    return f"Error: MongoDB update operation currently supports only exact match filters (eq) for field '{field_name}'. Rephrase your update query."

            # MongoDB's update_many requires $set operator for updating fields
            update_result = collection.update_many(mongo_filters, {'$set': new_data})
            
            if update_result.matched_count > 0:
                logging.info(f"Updated {update_result.modified_count} out of {update_result.matched_count} records in MongoDB collection '{table}'.")
                # To return updated documents, we need to query them again after update
                # This is less efficient but ensures we return the actual updated state.
                # A more efficient approach for very large updates might just return a success count.
                updated_docs = list(collection.find(mongo_filters).limit(update_result.modified_count))
                for doc in updated_docs:
                    if '_id' in doc:
                        doc['id'] = str(doc['_id'])
                        del doc['_id']
                return updated_docs
            else:
                return [] # No records matched filter
        except PyMongoError as pe:
            error_msg = f"Error updating records in MongoDB collection '{table}': {pe}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        except Exception as e:
            error_msg = f"Error updating records in MongoDB collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def delete_record(self, table: str, filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Deletes records from a MongoDB collection based on filters."""
        try:
            collection = self.db[table]
            mongo_filters = {}
            for field_name, condition in filters.items():
                op = condition.get('op')
                value = condition.get('value')

                # Special handling for 'id' which maps to '_id' in MongoDB
                if field_name == 'id':
                    from bson.objectid import ObjectId
                    if isinstance(value, str):
                        try:
                            value = ObjectId(value)
                        except:
                            logging.warning(f"Invalid ObjectId string for 'id' filter: {value}. Proceeding as string match.")
                    field_name = '_id'

                if op == 'eq':
                    mongo_filters[field_name] = value
                else:
                    logging.warning(f"MongoDB delete filter only supports 'eq' for now. Skipping filter '{field_name}' with op '{op}'.")
                    return f"Error: MongoDB delete operation currently supports only exact match filters (eq) for field '{field_name}'. Rephrase your delete query."

            # To return the deleted documents, we must find them *before* deletion
            documents_to_delete = list(collection.find(mongo_filters))
            
            delete_result = collection.delete_many(mongo_filters)
            
            if delete_result.deleted_count > 0:
                logging.info(f"Deleted {delete_result.deleted_count} records from MongoDB collection '{table}'.")
                for doc in documents_to_delete:
                    if '_id' in doc:
                        doc['id'] = str(doc['_id'])
                        del doc['_id']
                return documents_to_delete
            else:
                return [] # No records matched filter
        except PyMongoError as pe:
            error_msg = f"Error deleting records from MongoDB collection '{table}': {pe}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        except Exception as e:
            error_msg = f"Error deleting records from MongoDB collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def close(self):
        """Closes the MongoDB client connection."""
        if self.client:
            self.client.close()
            logging.info("MongoDB client connection closed.")