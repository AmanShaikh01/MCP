import logging
from typing import List, Dict, Any, Union
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
from psycopg2 import Error as Psycopg2Error

from utils.adapters.__init__ import BaseAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PostgreSQLAdapter(BaseAdapter):
    """
    PostgreSQL adapter for the universal query system.
    Handles PostgreSQL connections, schema introspection using information_schema,
    and query execution. Implements connection pooling.
    """

    # Using ThreadedConnectionPool for simplicity in a Flask app.
    # For highly concurrent async apps, consider asyncpg.
    _connection_pools: Dict[str, pool.ThreadedConnectionPool] = {}

    def __init__(self, connection_string: str):
        """
        Initializes the PostgreSQLAdapter.

        Args:
            connection_string (str): The PostgreSQL connection string.
                                     (e.g., "postgresql://user:password@host:port/database")
        """
        self.connection_string = connection_string
        self.pool_key = connection_string # Unique key for the pool

        if self.pool_key not in PostgreSQLAdapter._connection_pools:
            try:
                # minconn and maxconn can be adjusted based on expected load
                PostgreSQLAdapter._connection_pools[self.pool_key] = pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,
                    dsn=self.connection_string
                )
                logging.info(f"PostgreSQL connection pool created for {self.pool_key[:20]}...")
            except Psycopg2Error as e:
                logging.error(f"Failed to create PostgreSQL connection pool: {e}", exc_info=True)
                raise ConnectionError(f"PostgreSQL connection pool creation failed: {e}")
        
        self.pool = PostgreSQLAdapter._connection_pools[self.pool_key]
        self._test_initial_connection()

    def _get_conn(self):
        """Retrieves a connection from the pool."""
        try:
            return self.pool.getconn()
        except Psycopg2Error as e:
            logging.error(f"Failed to get connection from PostgreSQL pool: {e}", exc_info=True)
            raise ConnectionError(f"Failed to acquire PostgreSQL connection: {e}")

    def _put_conn(self, conn):
        """Returns a connection to the pool."""
        if conn:
            self.pool.putconn(conn)

    def _test_initial_connection(self):
        """Tests the connection immediately after pool creation."""
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            logging.info(f"PostgreSQL initial connection test successful for {self.pool_key[:20]}...")
        except Psycopg2Error as e:
            logging.error(f"PostgreSQL initial connection test failed: {e}", exc_info=True)
            raise ConnectionError(f"PostgreSQL initial connection test failed: {e}")
        finally:
            self._put_conn(conn)

    def test_connection(self) -> bool:
        """
        Tests the PostgreSQL connection by acquiring and releasing a connection from the pool.
        """
        conn = None
        try:
            conn = self._get_conn()
            # A simple query to ensure the connection is active
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            logging.info("PostgreSQL connection test successful.")
            return True
        except Psycopg2Error as e:
            logging.error(f"PostgreSQL connection test failed: {e}", exc_info=True)
            return False
        except Exception as e:
            logging.error(f"Unexpected error during PostgreSQL connection test: {e}", exc_info=True)
            return False
        finally:
            self._put_conn(conn)

    def get_table_names(self) -> List[str]:
        """
        Retrieves all public table names from PostgreSQL's information_schema.
        """
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                table_names = [row['table_name'] for row in cursor.fetchall()]
                logging.info(f"PostgreSQL discovered tables: {table_names}")
                return table_names
        except Psycopg2Error as e:
            logging.error(f"Error getting PostgreSQL table names: {e}", exc_info=True)
            return []
        finally:
            self._put_conn(conn)

    def get_column_info(self, table: str) -> List[Dict[str, str]]:
        """
        Retrieves column information for a specific PostgreSQL table using information_schema.
        """
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position;
                """, (table,))
                columns = [{'name': row['column_name'], 'type': row['data_type']} for row in cursor.fetchall()]
                logging.info(f"PostgreSQL discovered columns for {table}: {columns}")
                return columns
        except Psycopg2Error as e:
            logging.error(f"Error getting PostgreSQL column info for {table}: {e}", exc_info=True)
            return []
        finally:
            self._put_conn(conn)

    def execute_query(self, query_params: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a PostgreSQL query based on the provided query parameters.
        Constructs SQL dynamically. Uses parameterized queries for safety.
        """
        table = query_params.get('table')
        columns = query_params.get('columns', ['*'])
        filters = query_params.get('filters', {})
        limit = query_params.get('limit', 100)

        if not table:
            return "Error: Table name not provided for PostgreSQL query execution."

        sql_columns = ', '.join([f'"{col}"' for col in columns]) if columns and columns != ['*'] else '*'
        
        where_clauses = []
        params = []

        for col_name, condition in filters.items():
            op = condition.get('op')
            value = condition.get('value')

            if op == 'eq':
                where_clauses.append(f'"{col_name}" = %s')
                params.append(value)
            elif op == 'gt':
                where_clauses.append(f'"{col_name}" > %s')
                params.append(value)
            elif op == 'lt':
                where_clauses.append(f'"{col_name}" < %s')
                params.append(value)
            elif op == 'gte':
                where_clauses.append(f'"{col_name}" >= %s')
                params.append(value)
            elif op == 'lte':
                where_clauses.append(f'"{col_name}" <= %s')
                params.append(value)
            elif op == 'like':
                where_clauses.append(f'"{col_name}" ILIKE %s') # ILIKE for case-insensitive
                params.append(f'%{value}%')
            elif op == 'ilike':
                where_clauses.append(f'"{col_name}" ILIKE %s')
                params.append(f'%{value}%')
            elif op == 'in':
                if isinstance(value, list) and value:
                    placeholders = ', '.join(['%s'] * len(value))
                    where_clauses.append(f'"{col_name}" IN ({placeholders})')
                    params.extend(value)
                else:
                    logging.warning(f"PostgreSQL 'in' operator expects a non-empty list, got {type(value)} for {col_name}. Skipping filter.")
            elif op == 'nin':
                if isinstance(value, list) and value:
                    placeholders = ', '.join(['%s'] * len(value))
                    where_clauses.append(f'"{col_name}" NOT IN ({placeholders})')
                    params.extend(value)
                else:
                    logging.warning(f"PostgreSQL 'nin' operator expects a non-empty list, got {type(value)} for {col_name}. Skipping filter.")
            else:
                logging.warning(f"Unsupported operator '{op}' for PostgreSQL for column '{col_name}'. Skipping filter.")
                return f"Error: Unsupported operator '{op}' for PostgreSQL for column '{col_name}'."
        
        where_clause_str = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        sql_query = f'SELECT {sql_columns} FROM "{table}" {where_clause_str} LIMIT %s;'
        params.append(limit)

        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                logging.info(f"Executing PostgreSQL query: {sql_query} with params: {params}")
                cursor.execute(sql_query, tuple(params))
                results = [dict(row) for row in cursor.fetchall()]
                logging.info(f"PostgreSQL query executed successfully for '{table}'. Results: {len(results)}")
                return results
        except Psycopg2Error as e:
            error_msg = f"Error executing PostgreSQL query for table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        finally:
            self._put_conn(conn)

    def build_select_query(self, table: str, columns: List[str], filters: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """
        Builds a dictionary representing a PostgreSQL SELECT query.
        """
        return {
            'table': table,
            'columns': columns,
            'filters': filters,
            'limit': limit
        }

    def get_sample_records(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves sample records from a PostgreSQL table.
        """
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(f'SELECT * FROM "{table}" LIMIT %s;', (limit,))
                sample_data = [dict(row) for row in cursor.fetchall()]
                logging.info(f"PostgreSQL fetched {len(sample_data)} sample records from {table}.")
                return sample_data
        except Psycopg2Error as e:
            logging.error(f"Error getting PostgreSQL sample records for {table}: {e}", exc_info=True)
            return []
        finally:
            self._put_conn(conn)
    
    def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
        """
        Detects relationships (foreign keys) for a given PostgreSQL table
        by querying information_schema.
        """
        relationships = []
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("""
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
                """, (table,))
                
                for row in cursor.fetchall():
                    relationships.append({
                        'from_table': table,
                        'from_column': row['from_column'],
                        'to_table': row['to_table'],
                        'to_column': row['to_column'],
                        'type': 'one-to-many' # Most common FK type
                    })
            logging.info(f"PostgreSQL detected relationships for {table}: {relationships}")
            return relationships
        except Psycopg2Error as e:
            logging.error(f"Error detecting PostgreSQL relationships for {table}: {e}", exc_info=True)
            return []
        finally:
            self._put_conn(conn)

    def add_record(self, table: str, data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """Adds a new record to a PostgreSQL table."""
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                columns = ', '.join([f'"{k}"' for k in data.keys()])
                placeholders = ', '.join(['%s'] * len(data))
                sql = f'INSERT INTO "{table}" ({columns}) VALUES ({placeholders}) RETURNING *;'
                values = list(data.values())
                
                logging.info(f"Executing PostgreSQL INSERT: {sql} with values: {values}")
                cursor.execute(sql, values)
                conn.commit()
                inserted_record = dict(cursor.fetchone())
                logging.info(f"Added record to PostgreSQL table '{table}': {inserted_record}")
                return inserted_record
        except Psycopg2Error as e:
            if conn:
                conn.rollback()
            error_msg = f"Error adding record to PostgreSQL table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            if "duplicate key value violates unique constraint" in str(e).lower():
                return f"Error: A record with a conflicting unique key already exists in '{table}'."
            return error_msg
        finally:
            self._put_conn(conn)

    def update_record(self, table: str, filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Updates records in a PostgreSQL table based on filters."""
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                set_clauses = [f'"{k}" = %s' for k in new_data.keys()]
                set_values = list(new_data.values())

                where_clauses = []
                where_values = []
                for col_name, condition in filters.items():
                    op = condition.get('op')
                    value = condition.get('value')
                    # For updates, we usually expect simple equality filters for identification.
                    # Complex filters can be added but complicate the update syntax.
                    if op == 'eq':
                        where_clauses.append(f'"{col_name}" = %s')
                        where_values.append(value)
                    else:
                        logging.warning(f"PostgreSQL update filter only supports 'eq' for now. Skipping filter '{col_name}' with op '{op}'.")
                        return f"Error: PostgreSQL update operation currently supports only exact match filters (eq) for field '{col_name}'. Rephrase your update query."

                if not set_clauses:
                    return "Error: No data provided to update."
                if not where_clauses:
                    return "Error: No filters provided to identify records for update. Please provide specific criteria."

                sql = f'UPDATE "{table}" SET {", ".join(set_clauses)} WHERE {" AND ".join(where_clauses)} RETURNING *;'
                params = set_values + where_values
                
                logging.info(f"Executing PostgreSQL UPDATE: {sql} with params: {params}")
                cursor.execute(sql, params)
                conn.commit()
                updated_records = [dict(row) for row in cursor.fetchall()]
                logging.info(f"Updated {len(updated_records)} records in PostgreSQL table '{table}'.")
                return updated_records
        except Psycopg2Error as e:
            if conn:
                conn.rollback()
            error_msg = f"Error updating records in PostgreSQL table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        finally:
            self._put_conn(conn)

    def delete_record(self, table: str, filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """Deletes records from a PostgreSQL table based on filters."""
        conn = None
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                where_clauses = []
                where_values = []
                for col_name, condition in filters.items():
                    op = condition.get('op')
                    value = condition.get('value')
                    if op == 'eq':
                        where_clauses.append(f'"{col_name}" = %s')
                        where_values.append(value)
                    else:
                        logging.warning(f"PostgreSQL delete filter only supports 'eq' for now. Skipping filter '{col_name}' with op '{op}'.")
                        return f"Error: PostgreSQL delete operation currently supports only exact match filters (eq) for field '{col_name}'. Rephrase your delete query."

                if not where_clauses:
                    return "Error: No filters provided to identify records for deletion. Please provide specific criteria."
                
                sql = f'DELETE FROM "{table}" WHERE {" AND ".join(where_clauses)} RETURNING *;'
                params = where_values

                logging.info(f"Executing PostgreSQL DELETE: {sql} with params: {params}")
                cursor.execute(sql, params)
                conn.commit()
                deleted_records = [dict(row) for row in cursor.fetchall()]
                logging.info(f"Deleted {len(deleted_records)} records from PostgreSQL table '{table}'.")
                return deleted_records
        except Psycopg2Error as e:
            if conn:
                conn.rollback()
            error_msg = f"Error deleting records from PostgreSQL table '{table}': {e}"
            logging.error(error_msg, exc_info=True)
            return error_msg
        finally:
            self._put_conn(conn)

    def close(self):
        """Closes the connection pool for this specific DSN."""
        # This will close the pool for all instances using the same connection string.
        # This is a class-level operation.
        if self.pool_key in PostgreSQLAdapter._connection_pools:
            pool_to_close = PostgreSQLAdapter._connection_pools.pop(self.pool_key)
            pool_to_close.closeall()
            logging.info(f"PostgreSQL connection pool for {self.pool_key[:20]}... closed.")