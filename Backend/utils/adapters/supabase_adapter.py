import logging
from typing import List, Dict, Any, Union
from supabase import create_client, Client
from utils.adapters.__init__ import BaseAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SupabaseAdapter(BaseAdapter):
    """
    Supabase adapter for the universal query system.
    Handles Supabase-specific connections, schema introspection, and query execution.
    """

    def __init__(self, url: str, key: str):
        """
        Initializes the SupabaseAdapter.

        Args:
            url (str): The Supabase project URL.
            key (str): The Supabase anon key.
        """
        self.url = url
        self.key = key
        self.client: Client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initializes the Supabase client."""
        try:
            self.client = create_client(self.url, self.key)
            logging.info("Supabase client initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize Supabase client: {e}", exc_info=True)
            raise ConnectionError(f"Supabase initialization failed: {e}")

    def test_connection(self) -> bool:
        """
        Tests the Supabase connection by trying to fetch a very small set of data
        from an arbitrary public table or by checking the client's health.
        """
        try:
            # A simple way to test connection: try to list tables or fetch from a non-existent table to get a response
            # Supabase client doesn't have a direct 'ping' method for RLS-enabled tables.
            # We assume if we can list tables, the connection is okay.
            # This requires RLS to allow listing tables, or we can use a dummy table.
            # For simplicity, we try to get table names here.
            table_names = self.get_table_names()
            if table_names is not None: # It should return a list, even an empty one, on success
                logging.info("Supabase connection test successful.")
                return True
            return False
        except Exception as e:
            logging.error(f"Supabase connection test failed: {e}", exc_info=True)
            return False

    def get_table_names(self) -> List[str]:
        """
        Retrieves all public table names from Supabase.
        Uses PostgreSQL's information_schema.
        """
        try:
            # Query the PostgreSQL information_schema through Supabase
            response = self.client.from_('information_schema.tables').select('table_name').eq('table_schema', 'public').execute()
            if response.data:
                table_names = [d['table_name'] for d in response.data]
                logging.info(f"Supabase discovered tables: {table_names}")
                return table_names
            return []
        except Exception as e:
            logging.error(f"Error getting Supabase table names: {e}", exc_info=True)
            return []

    def get_column_info(self, table: str) -> List[Dict[str, str]]:
        """
        Retrieves column information for a specific Supabase table.
        Uses PostgreSQL's information_schema.
        """
        try:
            response = self.client.from_('information_schema.columns').select('column_name, data_type').eq('table_schema', 'public').eq('table_name', table).execute()
            if response.data:
                columns = [{'name': d['column_name'], 'type': d['data_type']} for d in response.data]
                logging.info(f"Supabase discovered columns for {table}: {columns}")
                return columns
            return []
        except Exception as e:
            logging.error(f"Error getting Supabase column info for {table}: {e}", exc_info=True)
            return []

    def execute_query(self, query_params: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a Supabase query based on the provided query parameters.
        """
        table = query_params.get('table')
        columns = query_params.get('columns', ['*'])
        filters = query_params.get('filters', {})
        limit = query_params.get('limit', 100)

        if not table:
            return "Error: Table name not provided for Supabase query execution."

        try:
            query = self.client.from_(table).select(', '.join(columns))

            for col_name, condition in filters.items():
                op = condition.get('op')
                value = condition.get('value')
                
                if op == 'eq':
                    query = query.eq(col_name, value)
                elif op == 'gt':
                    query = query.gt(col_name, value)
                elif op == 'lt':
                    query = query.lt(col_name, value)
                elif op == 'gte':
                    query = query.gte(col_name, value)
                elif op == 'lte':
                    query = query.lte(col_name, value)
                elif op == 'like':
                    query = query.ilike(col_name, f'%{value}%') # Supabase/Postgres uses ilike for case-insensitivity
                elif op == 'ilike':
                    query = query.ilike(col_name, f'%{value}%')
                elif op == 'in':
                    # Supabase 'in' operator expects a list of values
                    if isinstance(value, list):
                        query = query.in_(col_name, value)
                    else:
                        logging.warning(f"Supabase 'in' operator expects a list, got {type(value)} for {col_name}. Skipping filter.")
                elif op == 'nin':
                    if isinstance(value, list):
                        # Supabase doesn't have a direct 'nin'. We can use 'not.in_'.
                        query = query.not_.in_(col_name, value)
                    else:
                        logging.warning(f"Supabase 'nin' operator expects a list, got {type(value)} for {col_name}. Skipping filter.")
                else:
                    logging.warning(f"Unsupported operator '{op}' for Supabase for column '{col_name}'. Skipping filter.")

            response = query.limit(limit).execute()
            if response.data is None:
                return f"Error: No data received from Supabase for table '{table}'."
            logging.info(f"Supabase query executed successfully for '{table}'. Results: {len(response.data)}")
            return response.data
        except Exception as e:
            error_msg = f"Error executing Supabase query for table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def build_select_query(self, table: str, columns: List[str], filters: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """
        Builds a dictionary representing a Supabase SELECT query.
        """
        return {
            'table': table,
            'columns': columns,
            'filters': filters,
            'limit': limit
        }

    def get_sample_records(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves sample records from a Supabase table.
        """
        try:
            response = self.client.from_(table).select('*').limit(limit).execute()
            if response.data:
                logging.info(f"Supabase fetched {len(response.data)} sample records from {table}.")
                return response.data
            return []
        except Exception as e:
            logging.error(f"Error getting Supabase sample records for {table}: {e}", exc_info=True)
            return []
    
    def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
        """
        Detects relationships (foreign keys) for a given Supabase (PostgreSQL) table.
        Queries information_schema.
        """
        relationships = []
        try:
            # This is a complex query to get foreign key constraints in PostgreSQL
            query = """
            SELECT
                tc.constraint_name, kcu.column_name AS from_column,
                ccu.table_name AS to_table, ccu.column_name AS to_column
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s
            AND tc.table_schema = 'public';
            """
            # Supabase client doesn't directly support raw SQL execution for select.
            # We will use a workaround by assuming 'from_' can handle a pseudo-table with a raw query result or if a direct 'execute_raw_sql' was available.
            # For now, this is a limitation with current Supabase client's public interface for information_schema joins.
            # A more robust solution might involve direct psycopg2 for schema introspection, or creating a Supabase RPC function.
            # For the purpose of this mock, we'll return an empty list and log the limitation.
            logging.warning(f"Supabase client's `from_` method has limitations querying complex `information_schema` joins directly for relationships. Returning empty relationships for {table}.")
            # If the Supabase client had a `rpc` method or if we had a view set up:
            # response = self.client.rpc('get_foreign_keys_for_table', {'p_table_name': table}).execute()
            # For a simpler approach if we cannot run complex queries:
            # We would need to infer relationships based on column naming conventions (e.g., table_id)
            # or rely on the user to define them.
            
            # Example (conceptual): if Supabase allowed raw SQL for introspection
            # response = self.client.raw_sql(query, [table]).execute()
            # if response.data:
            #     for row in response.data:
            #         relationships.append({
            #             'from_table': table,
            #             'from_column': row['from_column'],
            #             'to_table': row['to_table'],
            #             'to_column': row['to_column'],
            #             'type': 'one-to-many' # Assuming for simplicity
            #         })

        except Exception as e:
            logging.error(f"Error detecting Supabase relationships for {table}: {e}", exc_info=True)
        return relationships

    def add_record(self, table: str, data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """Adds a new record to a Supabase table."""
        try:
            response = self.client.from_(table).insert(data).execute()
            if response.data:
                logging.info(f"Added record to Supabase table '{table}': {response.data[0]}")
                return response.data[0]
            return "Error: No data returned after insert. Record might not have been added."
        except Exception as e:
            error_msg = f"Error adding record to Supabase table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            # Check for common errors, e.g., duplicate key
            if "duplicate key value violates unique constraint" in str(e).lower():
                return f"Error: A record with a conflicting unique key already exists in '{table}'."
            return error_msg

    def update_record(self, table: str, filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Updates records in a Supabase table based on filters."""
        try:
            query = self.client.from_(table)
            for col_name, condition in filters.items():
                op = condition.get('op', 'eq') # Default to eq for update filters
                value = condition.get('value')
                if op == 'eq':
                    query = query.eq(col_name, value)
                else:
                    logging.warning(f"Supabase update filter only supports 'eq' for now. Skipping filter '{col_name}' with op '{op}'.")

            response = query.update(new_data).execute()
            if response.data:
                logging.info(f"Updated {len(response.data)} records in Supabase table '{table}'.")
                return response.data
            return [] # No records matched filter
        except Exception as e:
            error_msg = f"Error updating records in Supabase table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def delete_record(self, table: str, filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Deletes records from a Supabase table based on filters."""
        try:
            query = self.client.from_(table)
            for col_name, condition in filters.items():
                op = condition.get('op', 'eq') # Default to eq for delete filters
                value = condition.get('value')
                if op == 'eq':
                    query = query.eq(col_name, value)
                else:
                    logging.warning(f"Supabase delete filter only supports 'eq' for now. Skipping filter '{col_name}' with op '{op}'.")

            response = query.delete().execute()
            if response.data:
                logging.info(f"Deleted {len(response.data)} records from Supabase table '{table}'.")
                return response.data
            return [] # No records matched filter
        except Exception as e:
            error_msg = f"Error deleting records from Supabase table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg

    def close(self):
        """Supabase client doesn't require explicit close, connections are usually managed internally."""
        logging.info("Supabase adapter close method called (no explicit client close needed).")
        pass