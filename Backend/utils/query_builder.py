# import logging
# from typing import Dict, Any, List, Optional
# from utils.schema_inspector import SchemaInspector

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class QueryBuilder:
#     """
#     Universal Query Builder that works with any database adapter.
#     Builds queries from natural language filters, selects relevant columns,
#     and handles multi-table queries (though basic in Phase 1).
#     """

#     def __init__(self, db_adapter: Any, schema_inspector: SchemaInspector):
#         """
#         Initializes the QueryBuilder with a database adapter and schema inspector.

#         Args:
#             db_adapter (Any): An instance of a database adapter.
#             schema_inspector (SchemaInspector): An instance of SchemaInspector to access schema info.
#         """
#         self.db_adapter = db_adapter
#         self.schema_inspector = schema_inspector
#         self.schema = self.schema_inspector.discover_schema()

#     def build_query(self, filters: Dict[str, Any], table_name: Optional[str] = None, columns: Optional[List[str]] = None) -> Dict[str, Any]:
#         """
#         Main query builder method. Constructs a database-specific query based on
#         filters, target table, and requested columns.

#         Args:
#             filters (Dict[str, Any]): A dictionary of filters (e.g., {'column': {'op': 'eq', 'value': 'X'}}).
#             table_name (Optional[str]): The explicit name of the target table/collection. If None, it will be guessed.
#             columns (Optional[List[str]]): A list of columns to select. If None, all columns are selected.

#         Returns:
#             Dict[str, Any]: A dictionary representing the constructed query parameters,
#                             ready to be executed by the database adapter.
        
#         Raises:
#             ValueError: If the target table cannot be determined or filters are invalid.
#         """
#         target_table = table_name
#         if not target_table:
#             target_table = self.guess_table_from_filters(filters)
#             if not target_table:
#                 # If still no table, try the first table in the schema if available
#                 all_tables = self.schema_inspector.get_tables()
#                 if all_tables:
#                     target_table = all_tables[0]
#                     logging.info(f"No specific table found in filters, defaulting to first available table: {target_table}")
#                 else:
#                     raise ValueError("Could not determine target table for the query. Please specify a table.")

#         logging.info(f"Building query for table: {target_table} with filters: {filters}")

#         # Validate filters against the schema of the target table
#         self.validate_filters(filters, target_table)

#         # Determine relevant columns for selection
#         selected_columns = columns if columns is not None else self.get_relevant_columns(filters, target_table)

#         # Build the database-specific query structure
#         query_params = self.db_adapter.build_select_query(target_table, selected_columns, filters)

#         # Optimize the query (placeholder for future advanced optimizations)
#         optimized_query_params = self.optimize_query(query_params)
        
#         return optimized_query_params

#     def guess_table_from_filters(self, filters: Dict[str, Any]) -> Optional[str]:
#         """
#         Attempts to determine the target table/collection based on the column names in the filters.

#         Args:
#             filters (Dict[str, Any]): The filters provided by the natural language parser.

#         Returns:
#             Optional[str]: The guessed table name, or None if no clear table can be determined.
#         """
#         all_tables = self.schema_inspector.get_tables()
#         if not all_tables:
#             return None

#         # Simple heuristic: find the table that contains the most filter columns
#         table_scores: Dict[str, int] = {table: 0 for table in all_tables}
#         filter_columns = set(filters.keys())

#         for table in all_tables:
#             table_columns = {col['name'] for col in self.schema_inspector.get_columns(table)}
#             common_columns = filter_columns.intersection(table_columns)
#             table_scores[table] = len(common_columns)

#         # Find the table with the highest score
#         if table_scores:
#             best_table = max(table_scores, key=table_scores.get)
#             if table_scores[best_table] > 0:
#                 logging.info(f"Guessed table '{best_table}' based on filter columns.")
#                 return best_table
        
#         # If no filter columns match, try to guess from sample data or just return first table
#         if all_tables:
#             logging.info("Could not guess table from filters. Returning the first available table.")
#             return all_tables[0] # Fallback to first table if no clear guess
        
#         logging.warning("No tables available in schema to guess from.")
#         return None


#     def get_relevant_columns(self, filters: Dict[str, Any], table_name: str) -> List[str]:
#         """
#         Determines which columns are relevant to select based on the filters and potential user intent.
#         For now, returns all columns of the table. Can be enhanced later to be smarter.

#         Args:
#             filters (Dict[str, Any]): The filters applied to the query.
#             table_name (str): The name of the target table.

#         Returns:
#             List[str]: A list of column names to be selected.
#         """
#         columns_info = self.schema_inspector.get_columns(table_name)
#         if not columns_info:
#             return ['*'] # Return all if no schema info for columns

#         # For now, return all available columns.
#         # Future enhancement: prioritize columns mentioned in the query or common display columns.
#         return [col['name'] for col in columns_info]

#     def optimize_query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Applies basic query optimizations. Placeholder for more advanced logic (e.g.,
#         index usage, join optimization for multi-table queries).

#         Args:
#             query_params (Dict[str, Any]): The raw query parameters.

#         Returns:
#             Dict[str, Any]: Optimized query parameters.
#         """
#         # Example optimization: Add a default limit if not already present
#         if 'limit' not in query_params:
#             query_params['limit'] = 100 # Default limit to prevent large fetches
#             logging.info(f"Applied default limit of {query_params['limit']} to the query.")
#         return query_params

#     def validate_filters(self, filters: Dict[str, Any], table_name: str) -> None:
#         """
#         Validates the provided filters against the schema of the target table.

#         Args:
#             filters (Dict[str, Any]): The filters to validate.
#             table_name (str): The name of the target table.

#         Raises:
#             ValueError: If any filter column does not exist in the table schema or operator is invalid.
#         """
#         table_columns = {col['name']: col['type'] for col in self.schema_inspector.get_columns(table_name)}
        
#         supported_operators = ['eq', 'gt', 'lt', 'gte', 'lte', 'like', 'ilike', 'in', 'nin'] # Universal operators

#         for col_name, condition in filters.items():
#             if col_name not in table_columns:
#                 raise ValueError(f"Filter error: Column '{col_name}' does not exist in table '{table_name}'.")
            
#             op = condition.get('op')
#             value = condition.get('value')

#             if not op or not value:
#                 raise ValueError(f"Filter error for column '{col_name}': Missing operator or value.")

#             if op not in supported_operators:
#                 raise ValueError(f"Filter error for column '{col_name}': Unsupported operator '{op}'.")
            
#             # Basic type validation (can be more robust)
#             # Example: if table_columns[col_name] is numeric and value is not, or vice versa
#             # This requires more sophisticated type mapping and checking based on actual DB types.
#             logging.debug(f"Validated filter: {col_name} {op} {value}")