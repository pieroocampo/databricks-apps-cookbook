"""Tests for the database connector module using pytest best practices."""

import pandas as pd
import pytest

from services.db.connector import get_connection, query, close_connections


@pytest.fixture
def mock_sql(mocker):
    """Mock the databricks sql module."""
    return mocker.patch("services.db.connector.sql")


@pytest.fixture
def mock_cursor():
    """Create a mock cursor with test data."""

    class MockCursor:
        def __init__(self):
            self.execute_calls = []
            self.description = [("id",), ("name",)]
            self.result_data = [(1, "Test")]

        def execute(self, query):
            """Record query execution."""
            self.execute_calls.append(query)
            self.last_query = query

        def fetchall(self):
            """Return test data."""
            return self.result_data

    return MockCursor()


@pytest.fixture
def mock_db_connection(mocker, mock_cursor):
    """Create a mock database connection."""

    # Create a context manager that returns our cursor
    class MockCursorContextManager:
        def __enter__(self):
            return mock_cursor

        def __exit__(self, *args):
            pass

    # Create the connection mock
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = MockCursorContextManager()

    # Patch the get_connection function to return our mock
    mocker.patch("services.db.connector.get_connection", return_value=mock_conn)

    return mock_conn


class TestDatabaseConnector:
    """Tests for the database connector functionality."""

    def test_get_connection_creates_proper_connection(self, mock_sql):
        """Test that get_connection creates a connection with the correct parameters."""
        # Arrange
        warehouse_id = "test-warehouse-id"
        expected_http_path = f"/sql/1.0/warehouses/{warehouse_id}"

        # Act
        get_connection(warehouse_id)

        # Assert
        mock_sql.connect.assert_called_once()
        call_kwargs = mock_sql.connect.call_args.kwargs
        assert call_kwargs["http_path"] == expected_http_path

    def test_query_returns_dict_results(self, mock_db_connection, mock_cursor):
        """Test that query returns results as dictionaries when as_dict=True."""
        # Arrange
        test_query = "SELECT * FROM catalog.schema.table"

        # Act
        result = query(test_query, "warehouse-id", as_dict=True)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["name"] == "Test"
        assert test_query in mock_cursor.execute_calls

    def test_query_returns_dataframe(self, mock_db_connection, mock_cursor):
        """Test that query returns results as a DataFrame when as_dict=False."""
        # Arrange
        test_query = "SELECT * FROM catalog.schema.table"

        # Act
        result = query(test_query, "warehouse-id", as_dict=False)

        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["id"] == 1
        assert result.iloc[0]["name"] == "Test"
        assert test_query in mock_cursor.execute_calls

    def test_query_handles_exceptions(self, mocker):
        """Test that query properly handles and wraps exceptions."""
        # Arrange - create a connection that raises an exception when used
        mock_conn = mocker.MagicMock()

        class FailingCursorManager:
            def __enter__(self):
                raise ValueError("Database connection error")

            def __exit__(self, *args):
                pass

        mock_conn.cursor.return_value = FailingCursorManager()
        mocker.patch("services.db.connector.get_connection", return_value=mock_conn)

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            query("SELECT 1", "warehouse-id")

        assert "Query failed" in str(exc_info.value)
        assert "Database connection error" in str(exc_info.value)

    def test_close_connections_clears_cache(self, mocker):
        """Test that close_connections clears the connection cache."""
        # Arrange
        mock_cache_clear = mocker.patch.object(get_connection, "cache_clear")

        # Act
        close_connections()

        # Assert
        mock_cache_clear.assert_called_once()
