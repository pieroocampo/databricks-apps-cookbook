import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
from databricks.sdk import WorkspaceClient


workspace = WorkspaceClient()

def get_catalogs():
    catalogs = workspace.catalogs.list()
    # Parse metadata into a list of dictionaries
    catalogs_data = []
    for catalog in catalogs:
        catalogs_data.append({
            "Catalog Name": catalog.name,
            "Owner": catalog.owner,
            "Comment": catalog.comment,
            "Created At": datetime.datetime.fromtimestamp(catalog.created_at/1000),
            "Updated At": datetime.datetime.fromtimestamp(catalog.updated_at/1000),
        })    
    return pd.DataFrame(catalogs_data)

def get_schemas():
    schema_data = []
    for catalog in workspace.catalogs.list():
        schemas = workspace.schemas.list(catalog_name=catalog.name)
        for schema in schemas:
            print(schema.catalog_name)
            print(schema)
            schema_data.append({
                "Catalog Name": schema.catalog_name,
                "Catalog Type": schema.catalog_type,
                "Schema Name": schema.full_name,
                "Owner": schema.owner,
                "Comment": schema.comment,
                "Created At": datetime.datetime.fromtimestamp(schema.created_at/1000),
                "Updated At": datetime.datetime.fromtimestamp(schema.updated_at/1000),
                "Effective Predictive Optimization": schema.effective_predictive_optimization_flag,
                "Properites": schema.properties

            })
    return pd.DataFrame(schema_data)



st.header(body="Unity Catalog", divider=True)
st.subheader("Get catalog and schema information")
st.write(
    "This receipt gets the meta data for the catalogs and the schemas."
)

tab_a, tab_b = st.tabs(["**Try it**", "**Code snippets**"])

with tab_a:
    if st.button("Try It"):
        st.write('### Databricks Catalogs')
        st.dataframe(get_catalogs())

        st.write('### Databricks Schema')
        
        schemas = get_schemas()
        st.dataframe(schemas)


table = [
    {
        "type": "Get Catalog",
        "param": "get_catalog",
        "description": "Get the catalogs.",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient


        workspace = WorkspaceClient()

        def get_catalogs():
            catalogs = workspace.catalogs.list()
            # Parse metadata into a list of dictionaries
            catalogs_data = []
            for catalog in catalogs:
                catalogs_data.append({
                    "Catalog Name": catalog.name,
                    "Owner": catalog.owner,
                    "Comment": catalog.comment,
                    "Created At": datetime.datetime.fromtimestamp(catalog.created_at/1000),
                    "Updated At": datetime.datetime.fromtimestamp(catalog.updated_at/1000),
                })    
            return pd.DataFrame(catalogs_data)
        st.write('### Databricks Catalogs')
        st.dataframe(get_catalogs())
        ```
        """,
    },
    {
        "type": "Get Schemas",
        "param": "get_schemas",
        "description": "Get the schemas",
        "code": """
        ```python
        from databricks.sdk import WorkspaceClient
        
        workspace = WorkspaceClient()
                
        def get_schemas():
            schema_data = []
            for catalog in workspace.catalogs.list():
                schemas = workspace.schemas.list(catalog_name=catalog.name)
                for schema in schemas:
                    print(schema.catalog_name)
                    print(schema)
                    schema_data.append({
                        "Catalog Name": schema.catalog_name,
                        "Catalog Type": schema.catalog_type,
                        "Schema Name": schema.full_name,
                        "Owner": schema.owner,
                        "Comment": schema.comment,
                        "Created At": datetime.datetime.fromtimestamp(schema.created_at/1000),
                        "Updated At": datetime.datetime.fromtimestamp(schema.updated_at/1000),
                        "Effective Predictive Optimization": schema.effective_predictive_optimization_flag,
                        "Properites": schema.properties

                    })
            return pd.DataFrame(schema_data)
        schemas = get_schemas()
        st.dataframe(schemas)
        ```
        """,
    },
]

with tab_b:
    for i, row in enumerate(table):
        with st.expander(f"**{row['type']} ({row['param']})**", expanded=(i == 0)):
            st.markdown(f"**Description**: {row['description']}")
            st.markdown(row["code"])
