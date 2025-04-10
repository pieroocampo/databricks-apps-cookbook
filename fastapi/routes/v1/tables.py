"""
Endpoints for interacting with Databricks tables.

This module provides endpoints for querying data from
Databricks Unity Catalog tables.
"""

from fastapi import APIRouter, Depends, Query

from config.settings import Settings, get_settings
from errors.exceptions import ConfigurationError, DatabaseError
from models.tables import TableQueryParams, TableResponse
from services.db.connector import query_table

router = APIRouter(tags=["tables"])


@router.get("/table", response_model=TableResponse)
async def table(
    catalog: str = Query(..., description="The catalog name"),
    schema: str = Query(..., description="The schema name"),
    table: str = Query(..., description="The table name"),
    limit: int = Query(100, description="Maximum number of records to return"),
    offset: int = Query(0, description="Number of records to skip"),
    columns: str = Query(
        "*", description="Comma-separated list of columns to retrieve"
    ),
    filter_expr: str = Query(None, description="Optional SQL WHERE clause"),
    settings: Settings = Depends(get_settings),
) -> TableResponse:
    """
    Retrieve data from a Unity Catalog table with filtering and pagination.

    Args:
        catalog: The catalog name
        schema: The schema name
        table: The table name
        limit: Maximum number of records to return
        offset: Number of records to skip
        columns: Comma-separated list of columns to retrieve
        filter_expr: Optional SQL WHERE clause
        settings: Application settings

    Returns:
        TableResponse containing the requested data

    Raises:
        ConfigurationError: If the SQL warehouse ID is not configured
        DatabaseError: If the query fails
    """
    # Validate query parameters using Pydantic model
    params = TableQueryParams(
        catalog=catalog,
        schema=schema,  # This will be mapped to schema_name via alias
        table=table,
        limit=limit,
        offset=offset,
        columns=columns,
        filter_expr=filter_expr,
    )

    # Get warehouse ID from settings
    warehouse_id = settings.databricks_warehouse_id
    if not warehouse_id:
        raise ConfigurationError(
            message="SQL warehouse ID not configured",
            details={"setting": "databricks_warehouse_id"},
        )

    try:
        # Build the SQL query
        table_path = f"{params.catalog}.{params.schema_name}.{params.table}"
        where_clause = f"WHERE {params.filter_expr}" if params.filter_expr else ""

        query = f"""
            SELECT {params.columns}
            FROM {table_path}
            {where_clause}
            LIMIT {params.limit} OFFSET {params.offset}
        """

        # Execute the query
        results = query_table(query, warehouse_id=warehouse_id)

        # Create the response
        return TableResponse(
            data=results,
            count=len(results),
            # Total is not available without an additional count query
            total=None,
        )
    except Exception as e:
        # Wrap any exceptions in a DatabaseError
        raise DatabaseError(
            message=f"Failed to query table: {str(e)}",
            details={
                "catalog": params.catalog,
                "schema": params.schema_name,
                "table": params.table,
            },
        )
