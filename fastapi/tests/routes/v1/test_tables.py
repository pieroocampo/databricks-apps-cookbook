"""Tests for the tables module using pure pytest techniques."""

import pytest

# Import the function to test directly
from routes.v1.tables import table

# Import needed dependencies
from config.settings import Settings
from errors.exceptions import ConfigurationError, DatabaseError


@pytest.fixture
def mock_settings():
    """Create settings with a test warehouse ID."""
    settings = Settings()
    settings.databricks_warehouse_id = "test-warehouse-123"
    return settings


@pytest.fixture
def mock_settings_no_warehouse():
    """Create settings with no warehouse ID."""
    settings = Settings()
    settings.databricks_warehouse_id = None
    return settings


@pytest.fixture
def mock_query_result():
    """Factory fixture for query results."""

    def _create_data(data=None):
        return data or [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]

    return _create_data


@pytest.mark.asyncio
class TestTableFunction:
    """Test suite for table function directly."""

    async def test_table_function_success(
        self, mock_settings, mock_query_result, monkeypatch
    ):
        """Test successful table query with valid warehouse ID."""
        # Setup
        test_data = mock_query_result()

        # Create a test function to replace query_table
        def mock_query(sql_query, warehouse_id, as_dict=True):
            assert "test_catalog.test_schema.test_table" in sql_query
            assert "LIMIT 10 OFFSET 0" in sql_query
            assert warehouse_id == "test-warehouse-123"
            return test_data

        # Apply the monkeypatch
        monkeypatch.setattr("routes.v1.tables.query_table", mock_query)

        # Call function directly
        result = await table(
            catalog="test_catalog",
            schema="test_schema",
            table="test_table",
            limit=10,
            offset=0,
            columns="id,name",
            filter_expr=None,
            settings=mock_settings,
        )

        # Assert result
        assert result.data == test_data
        assert result.count == 2
        assert result.total is None

    async def test_table_function_missing_warehouse(self, mock_settings_no_warehouse):
        """Test function raises error when warehouse ID is missing."""
        # Call function and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            await table(
                catalog="test_catalog",
                schema="test_schema",
                table="test_table",
                limit=10,
                offset=0,
                columns="*",
                filter_expr=None,
                settings=mock_settings_no_warehouse,
            )

        # Assert exception details
        assert "SQL warehouse ID not configured" in str(exc_info.value)

    async def test_table_function_database_error(self, mock_settings, monkeypatch):
        """Test function handles database errors correctly."""

        # Setup - create a function that raises an exception
        def mock_query_error(*args, **kwargs):
            raise Exception("Database connection failed")

        # Apply the monkeypatch
        monkeypatch.setattr("routes.v1.tables.query_table", mock_query_error)

        # Call function and expect exception
        with pytest.raises(DatabaseError) as exc_info:
            await table(
                catalog="test_catalog",
                schema="test_schema",
                table="test_table",
                limit=10,
                offset=0,
                columns="*",
                filter_expr=None,
                settings=mock_settings,
            )

        # Assert exception details
        assert "Failed to query table" in str(exc_info.value)

    async def test_table_function_with_filter(self, mock_settings, monkeypatch):
        """Test function with filter expression."""
        # Setup - create specific test data for this test
        filter_test_data = [{"id": 6, "timestamp": "2025-04-01"}]

        # Create a test function with assertions
        def mock_query_with_filter(sql_query, warehouse_id, as_dict=True):
            assert "WHERE id > 5 AND timestamp > '2025-04-01'" in sql_query
            assert "LIMIT 20 OFFSET 10" in sql_query
            return filter_test_data

        # Apply the monkeypatch
        monkeypatch.setattr("routes.v1.tables.query_table", mock_query_with_filter)

        # Call function with filter
        result = await table(
            catalog="test_catalog",
            schema="test_schema",
            table="test_table",
            limit=20,
            offset=10,
            columns="id,timestamp",
            filter_expr="id > 5 AND timestamp > '2025-04-01'",
            settings=mock_settings,
        )

        # Assert result
        assert len(result.data) == 1
        assert result.count == 1
