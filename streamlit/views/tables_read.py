import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

st.header(body="Tables", divider=True)
st.subheader("Read a table")
st.write(
    "This recipe reads a Unity Catalog table using the [Databricks SQL Connector](https://docs.databricks.com/en/dev-tools/python-sql-connector.html)."
)

cfg = Config()


@st.cache_resource
def get_connection(http_path):
    return sql.connect(
        server_hostname=cfg.host,
        http_path=http_path,
        credentials_provider=lambda: cfg.authenticate,
    )


def read_table(table_name, conn):
    with conn.cursor() as cursor:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        return cursor.fetchall_arrow().to_pandas()


tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

with tab_a:
    http_path_input = st.text_input(
        "Enter your Databricks HTTP Path:", placeholder="/sql/1.0/warehouses/xxxxxx"
    )

    table_name = st.text_input(
        "Specify a Unity Catalog table name:", placeholder="catalog.schema.table"
    )

    if http_path_input and table_name:
        conn = get_connection(http_path_input)
        df = read_table(table_name, conn)
        st.dataframe(df)

with tab_b:
    st.code(
        """
        import streamlit as st
        from databricks import sql
        from databricks.sdk.core import Config


        cfg = Config()  # Set the DATABRICKS_HOST environment variable when running locally


        @st.cache_resource
        def get_connection(http_path):
            return sql.connect(
                server_hostname=cfg.host,
                http_path=http_path,
                credentials_provider=lambda: cfg.authenticate,
            )


        def read_table(table_name, conn):
            with conn.cursor() as cursor:
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)
                return cursor.fetchall_arrow().to_pandas()


        http_path_input = st.text_input(
            "Enter your Databricks HTTP Path:", placeholder="/sql/1.0/warehouses/xxxxxx"
        )

        table_name = st.text_input(
            "Specify a Unity Catalog table name:", placeholder="catalog.schema.table"
        )

        if http_path_input and table_name:
            conn = get_connection(http_path_input)
            df = read_table(table_name, conn)
            st.dataframe(df)
        """
    )

with tab_c:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
                    **Permissions (app service principal)**
                    * `SELECT` on the Unity Catalog table
                    * `CAN USE` on the SQL warehouse
                    """)
    with col2:
        st.markdown("""
                    **Databricks resources**
                    * SQL warehouse
                    * Unity Catalog table
                    """)
    with col3:
        st.markdown("""
                    **Dependencies**
                    * [Databricks SDK](https://pypi.org/project/databricks-sdk/) - `databricks-sdk`
                    * [Databricks SQL Connector](https://pypi.org/project/databricks-sql-connector/) - `databricks-sql-connector`
                    * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
                    """)
