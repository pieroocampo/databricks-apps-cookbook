# FastAPI Example for Databricks Apps

This is a sample FastAPI application that demonstrates how API-based applications can be deployed on Databricks Apps runtime.  
The sample application is headless and intended to be used with bearer token authentication (OAuth2).

Please refer to [Databricks authorization methods](https://docs.databricks.com/aws/en/dev-tools/auth/#databricks-authorization-methods) to obtain an OAuth token appropriately.

## API Endpoints

The sample application provides the following API endpoints:

#### API v1
- `/api/v1/healthcheck` - Returns a response to validate the health of the application
- `/api/v1/table` - Query data from Databricks tables

#### Documentation
- `/docs` - Interactive OpenAPI documentation

## Running Locally

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies within active venv
pip install -r requirements.txt

# Set environment variables (if not using .env file)
export DATABRICKS_WAREHOUSE_ID=your-warehouse-id

# Run the application
uvicorn app:app --reload
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/v1/test_healthcheck.py
```

## Configuration

The application uses environment variables for configuration:

- `DATABRICKS_WAREHOUSE_ID` - The ID of the Databricks SQL warehouse
- `DATABRICKS_HOST` - (Optional) The Databricks workspace host
- `DATABRICKS_TOKEN` - (Optional) The Databricks access token