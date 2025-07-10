import logging
from typing import List, Dict, Any, Union
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.api_core.exceptions import GoogleAPIError, NotFound

from utils.adapters.__init__ import BaseAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FirebaseAdapter(BaseAdapter):
    """
    Firebase Firestore adapter for the universal query system.
    Handles Firebase-specific connections, schema introspection (for collections),
    and query execution for Firestore documents.
    """

    def __init__(self, credentials_path: str):
        """
        Initializes the FirebaseAdapter.

        Args:
            credentials_path (str): Path to the Firebase service account key file (JSON).
        """
        self.credentials_path = credentials_path
        self.db: firestore.Client = None
        self._initialize_app()

    def _initialize_app(self):
        """Initializes the Firebase Admin SDK app and Firestore client."""
        try:
            if not firebase_admin._apps: # Initialize only if not already initialized
                cred = credentials.Certificate(self.credentials_path)
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            logging.info("Firebase Admin SDK and Firestore client initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize Firebase: {e}", exc_info=True)
            raise ConnectionError(f"Firebase initialization failed: {e}. Check credentials path: {self.credentials_path}")

    def test_connection(self) -> bool:
        """
        Tests the Firebase Firestore connection by attempting to list some collections.
        Firebase client doesn't have a direct 'ping'. Listing collections is a good test.
        """
        try:
            # Attempt to list 1 top-level collection to confirm connection
            # Note: list_collections() requires appropriate permissions.
            collections_iterator = self.db.collections()
            first_collection = next(collections_iterator, None)
            if first_collection:
                logging.info(f"Firebase connection test successful. Found collection: {first_collection.id}")
            else:
                logging.info("Firebase connection successful, but no top-level collections found.")
            return True
        except Exception as e:
            logging.error(f"Firebase connection test failed: {e}", exc_info=True)
            return False

    def get_table_names(self) -> List[str]:
        """
        Retrieves all top-level collection names from Firestore.
        Firestore doesn't have a direct "list all collections" API that scales for very large numbers
        without iterating. For free tier/small apps, this is usually sufficient.
        """
        try:
            collections = [col.id for col in self.db.collections()]
            logging.info(f"Firebase discovered collections: {collections}")
            return collections
        except Exception as e:
            logging.error(f"Error getting Firebase collection names: {e}", exc_info=True)
            return []

    def get_column_info(self, table: str) -> List[Dict[str, str]]:
        """
        Infers 'column' (field) information for a Firestore collection by inspecting sample documents.
        Firestore is schemaless, so this is an inference, not a fixed schema.
        """
        columns_info = []
        try:
            sample_docs = self.get_sample_records(table, limit=5) # Get a few samples
            seen_fields = set()
            for doc in sample_docs:
                for field_name, field_value in doc.items():
                    if field_name not in seen_fields:
                        # Infer type (basic inference)
                        field_type = type(field_value).__name__
                        if isinstance(field_value, dict):
                            field_type = 'map'
                        elif isinstance(field_value, list):
                            field_type = 'array'
                        elif isinstance(field_value, int):
                            field_type = 'integer'
                        elif isinstance(field_value, float):
                            field_type = 'float'
                        elif isinstance(field_value, bool):
                            field_type = 'boolean'
                        elif isinstance(field_value, str):
                            field_type = 'string'
                        
                        columns_info.append({'name': field_name, 'type': field_type})
                        seen_fields.add(field_name)
            
            logging.info(f"Firebase inferred columns for {table}: {columns_info}")
            return columns_info
        except Exception as e:
            logging.error(f"Error inferring Firebase column info for {table}: {e}", exc_info=True)
            return []

    def execute_query(self, query_params: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a Firestore query based on the provided parameters.
        """
        table = query_params.get('table')
        # Firestore queries implicitly select all fields of a document
        # columns = query_params.get('columns', ['*']) # Not directly applicable in Firestore for selection
        filters = query_params.get('filters', {})
        limit = query_params.get('limit', 100)

        if not table:
            return "Error: Collection name not provided for Firebase query execution."

        try:
            query = self.db.collection(table)

            for field_name, condition in filters.items():
                op = condition.get('op')
                value = condition.get('value')

                if op == 'eq':
                    query = query.where(filter=FieldFilter(field_name, "==", value))
                elif op == 'gt':
                    query = query.where(filter=FieldFilter(field_name, ">", value))
                elif op == 'lt':
                    query = query.where(filter=FieldFilter(field_name, "<", value))
                elif op == 'gte':
                    query = query.where(filter=FieldFilter(field_name, ">=", value))
                elif op == 'lte':
                    query = query.where(filter=FieldFilter(field_name, "<=", value))
                elif op == 'like':
                    # Firestore does not support direct 'like' operator for partial string matching.
                    # This would require more complex solutions (e.g., full-text search with Algolia, or fetching all and filtering in-memory).
                    # For a simple 'starts with', you could do: .where(field, '>=', value).where(field, '<', value + '\uf8ff')
                    logging.warning(f"Firestore does not support 'like' operator directly. Skipping filter for '{field_name}'.")
                    return f"Error: Partial string matching (like operator) is not directly supported by Firestore for field '{field_name}'. Consider exact matches."
                elif op == 'in':
                    if isinstance(value, list) and len(value) <= 10: # Firestore 'in' has a limit of 10 values
                        query = query.where(filter=FieldFilter(field_name, "in", value))
                    else:
                        logging.warning(f"Firestore 'in' operator expects a list of up to 10 values. Got {len(value)} for {field_name}. Skipping filter.")
                        return f"Error: Firestore 'in' operator supports a maximum of 10 values. Please reduce the list for field '{field_name}'."
                elif op == 'nin':
                    # Firestore does not support 'not in' operator directly
                    logging.warning(f"Firestore does not support 'not in' operator directly. Skipping filter for '{field_name}'.")
                    return f"Error: 'Not in' operator is not directly supported by Firestore for field '{field_name}'."
                else:
                    logging.warning(f"Unsupported operator '{op}' for Firestore for field '{field_name}'. Skipping filter.")
                    return f"Error: Unsupported operator '{op}' for Firestore for field '{field_name}'."

            docs = query.limit(limit).stream()
            results = []
            for doc in docs:
                data = doc.to_dict()
                if data:
                    data['id'] = doc.id # Include document ID
                    results.append(data)
            
            logging.info(f"Firestore query executed successfully for '{table}'. Results: {len(results)}")
            return results
        except GoogleAPIError as ge:
            error_msg = f"Firestore API error executing query for collection '{table}': {ge.code} - {ge.message}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        except Exception as e:
            error_msg = f"Error executing Firebase query for collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def build_select_query(self, table: str, columns: List[str], filters: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """
        Builds a dictionary representing a Firebase Firestore query.
        For Firestore, 'columns' are mostly ignored as queries return full documents.
        """
        return {
            'table': table,
            'filters': filters,
            'limit': limit
        }

    def get_sample_records(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves sample documents from a Firestore collection.
        """
        try:
            docs = self.db.collection(table).limit(limit).stream()
            sample_data = []
            for doc in docs:
                data = doc.to_dict()
                if data:
                    data['id'] = doc.id # Include document ID
                    sample_data.append(data)
            
            logging.info(f"Firebase fetched {len(sample_data)} sample records from {table}.")
            return sample_data
        except NotFound:
            logging.warning(f"Collection '{table}' not found in Firebase.")
            return []
        except Exception as e:
            logging.error(f"Error getting Firebase sample records for {table}: {e}", exc_info=True)
            return []
    
    def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
        """
        Detects relationships in Firestore. This is generally not straightforward as Firestore
        is NoSQL. Relationships are often implied by document references or nested collections.
        For Phase 1, we will return an empty list. Advanced versions could try to infer
        from field names ending in '_id' or looking for DocumentReference types.
        """
        logging.info(f"Firestore does not have explicit foreign key relationships like relational databases. Relationships for '{table}' need to be inferred or manually defined. Returning empty list for now.")
        return []

    def add_record(self, table: str, data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """Adds a new document to a Firestore collection."""
        try:
            # If 'id' is in data, try to use it as document ID
            doc_id = data.pop('id', None) 
            if doc_id:
                doc_ref = self.db.collection(table).document(str(doc_id))
            else:
                doc_ref = self.db.collection(table).document() # Auto-generate ID

            doc_ref.set(data) # set() will create or overwrite
            
            inserted_data = data.copy()
            inserted_data['id'] = doc_ref.id
            logging.info(f"Added record to Firestore collection '{table}' with ID: {doc_ref.id}")
            return inserted_data
        except Exception as e:
            error_msg = f"Error adding record to Firestore collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def update_record(self, table: str, filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Updates documents in a Firestore collection based on filters."""
        try:
            if not filters:
                return "Error: Update operation requires filters to specify which documents to update in Firestore."

            # Firebase updates usually target specific documents.
            # If the filter specifies an 'id', we can directly update that document.
            doc_id_filter = filters.get('id')
            if doc_id_filter and doc_id_filter.get('op') == 'eq':
                doc_id = doc_id_filter.get('value')
                doc_ref = self.db.collection(table).document(str(doc_id))
                try:
                    doc_ref.update(new_data)
                    updated_doc = doc_ref.get()
                    if updated_doc.exists:
                        data = updated_doc.to_dict()
                        if data:
                            data['id'] = updated_doc.id
                            logging.info(f"Updated single record in Firestore collection '{table}' with ID: {doc_id}")
                            return [data]
                    return [] # Document not found after update
                except NotFound:
                    return f"Error: Document with ID '{doc_id}' not found in collection '{table}'."
            else:
                # For non-ID based filters, we need to query first, then update each document.
                # This can be expensive and hit limits for large result sets.
                query = self.db.collection(table)
                for field_name, condition in filters.items():
                    op = condition.get('op')
                    value = condition.get('value')
                    # Firebase update queries typically support 'eq', '>', '<', '>=', '<='
                    # We might limit to 'eq' for simplicity in updates.
                    if op == 'eq':
                        query = query.where(filter=FieldFilter(field_name, "==", value))
                    else:
                        logging.warning(f"Firestore update operation currently supports only 'eq' filter. Skipping complex filter for '{field_name}'.")
                        return f"Error: For updates, Firestore currently supports only exact match filters (eq) for field '{field_name}'. Rephrase your update query."

                batch = self.db.batch()
                updated_docs_list = []
                for doc in query.stream():
                    batch.update(doc.reference, new_data)
                    updated_data = doc.to_dict()
                    updated_data.update(new_data)
                    updated_data['id'] = doc.id
                    updated_docs_list.append(updated_data)
                
                if updated_docs_list:
                    batch.commit()
                    logging.info(f"Updated {len(updated_docs_list)} records in Firestore collection '{table}'.")
                    return updated_docs_list
                else:
                    return [] # No records matched filter

        except Exception as e:
            error_msg = f"Error updating records in Firestore collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def delete_record(self, table: str, filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Deletes documents from a Firestore collection based on filters."""
        try:
            if not filters:
                return "Error: Delete operation requires filters to specify which documents to delete in Firestore."

            # If the filter specifies an 'id', we can directly delete that document.
            doc_id_filter = filters.get('id')
            if doc_id_filter and doc_id_filter.get('op') == 'eq':
                doc_id = doc_id_filter.get('value')
                doc_ref = self.db.collection(table).document(str(doc_id))
                try:
                    doc_data_before_delete = doc_ref.get()
                    doc_ref.delete()
                    if doc_data_before_delete.exists:
                        data = doc_data_before_delete.to_dict()
                        if data:
                            data['id'] = doc_data_before_delete.id
                            logging.info(f"Deleted single record from Firestore collection '{table}' with ID: {doc_id}")
                            return [data]
                    return [] # Document not found before delete
                except NotFound:
                    return f"Error: Document with ID '{doc_id}' not found for deletion in collection '{table}'."
            else:
                # For non-ID based filters, we need to query first, then delete each document.
                query = self.db.collection(table)
                for field_name, condition in filters.items():
                    op = condition.get('op')
                    value = condition.get('value')
                    if op == 'eq':
                        query = query.where(filter=FieldFilter(field_name, "==", value))
                    else:
                        logging.warning(f"Firestore delete operation currently supports only 'eq' filter. Skipping complex filter for '{field_name}'.")
                        return f"Error: For deletions, Firestore currently supports only exact match filters (eq) for field '{field_name}'. Rephrase your delete query."

                batch = self.db.batch()
                deleted_docs_list = []
                for doc in query.stream():
                    batch.delete(doc.reference)
                    data = doc.to_dict()
                    if data:
                        data['id'] = doc.id
                        deleted_docs_list.append(data)
                
                if deleted_docs_list:
                    batch.commit()
                    logging.info(f"Deleted {len(deleted_docs_list)} records from Firestore collection '{table}'.")
                    return deleted_docs_list
                else:
                    return [] # No records matched filter

        except Exception as e:
            error_msg = f"Error deleting records from Firestore collection '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def close(self):
        """Firebase Admin SDK doesn't require explicit close of the db client."""
        logging.info("Firebase adapter close method called (no explicit client close needed).")
        pass