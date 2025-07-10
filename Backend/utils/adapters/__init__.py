from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

class BaseAdapter(ABC):
    """
    Abstract Base Class for all database adapters.
    Defines the universal interface for database interactions.
    """

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Verifies if the connection to the database is working.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_table_names(self) -> List[str]:
        """
        Lists all table/collection names available in the database.

        Returns:
            List[str]: A list of table/collection names.
        """
        pass

    @abstractmethod
    def get_column_info(self, table: str) -> List[Dict[str, str]]:
        """
        Retrieves column/field information for a specific table/collection.

        Args:
            table (str): The name of the table or collection.

        Returns:
            List[Dict[str, str]]: A list of dictionaries, each with 'name' and 'type' of the column.
                                   Example: [{'name': 'id', 'type': 'integer'}, {'name': 'name', 'type': 'text'}]
        """
        pass

    @abstractmethod
    def execute_query(self, query_params: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a structured query built by the QueryBuilder.

        Args:
            query_params (Dict[str, Any]): A dictionary containing parameters for the query.
                                            Expected keys: 'table', 'columns', 'filters', 'limit', etc.

        Returns:
            Union[List[Dict[str, Any]], str]: A list of dictionaries representing the query results,
                                               or an error string if the query fails.
        """
        pass

    @abstractmethod
    def build_select_query(self, table: str, columns: List[str], filters: Dict[str, Any], limit: int = 100) -> Dict[str, Any]:
        """
        Builds a database-specific SELECT query structure based on universal parameters.
        This method should return a dictionary representing the query, not execute it.
        The `execute_query` method will consume this dictionary.

        Args:
            table (str): The name of the table/collection.
            columns (List[str]): List of column names to select (e.g., ['name', 'age']). Use '*' for all.
            filters (Dict[str, Any]): Dictionary of filters (e.g., {'age': {'op': 'gt', 'value': 25}}).
            limit (int): Maximum number of records to return.

        Returns:
            Dict[str, Any]: A database-specific representation of the query to be executed.
        """
        pass

    @abstractmethod
    def get_sample_records(self, table: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves a small number of sample records from a table/collection.

        Args:
            table (str): The name of the table or collection.
            limit (int): The maximum number of sample records to retrieve.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a sample record.
        """
        pass
    
    @abstractmethod
    def detect_relationships(self, table: str) -> List[Dict[str, Any]]:
        """
        Detects relationships (e.g., foreign keys) for a given table.
        This might involve querying system tables or inferring from column names.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries describing relationships.
                                   Example: [{'from_table': 'orders', 'from_column': 'customer_id',
                                              'to_table': 'customers', 'to_column': 'id', 'type': 'one-to-many'}]
        """
        pass

    @abstractmethod
    def add_record(self, table: str, data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Adds a new record to the specified table/collection.

        Args:
            table (str): The name of the table/collection.
            data (Dict[str, Any]): The data to insert.

        Returns:
            Union[Dict[str, Any], str]: The inserted record (or its ID/confirmation) or an error string.
        """
        pass

    @abstractmethod
    def update_record(self, table: str, filters: Dict[str, Any], new_data: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Updates existing records in the specified table/collection based on filters.

        Args:
            table (str): The name of the table/collection.
            filters (Dict[str, Any]): The criteria to identify records to update.
            new_data (Dict[str, Any]): The new values to set for the matching records.

        Returns:
            Union[List[Dict[str, Any]], str]: A list of updated records (or confirmation) or an error string.
        """
        pass

    @abstractmethod
    def delete_record(self, table: str, filters: Dict[str, Any]) -> Union[List[Dict[str, Any]], str]:
        """
        Deletes records from the specified table/collection based on filters.

        Args:
            table (str): The name of the table/collection.
            filters (Dict[str, Any]): The criteria to identify records to delete.

        Returns:
            Union[List[Dict[str, Any]], str]: A list of deleted records (or confirmation) or an error string.
        """
        pass

    def close(self):
        """
        Closes any open database connections or releases resources.
        Implement in subclasses if connection needs explicit closing.
        """
        pass