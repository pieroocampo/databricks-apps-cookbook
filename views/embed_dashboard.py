import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from databricks.connect import DatabricksSession

st.header("Compute", divider=True)
st.subheader("Connect")
st.write(
    """
    This recipe uses [Databricks Connect](https://docs.databricks.com/en/dev-tools/databricks-connect/python/index.html) to execute pre-defined Python or SQL code on a **shared** cluster with UI inputs. 
    """
)
tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

server_hostname = os.getenv("DATABRICKS_HOST") or os.getenv("DATABRICKS_HOSTNAME")


def connect_to_cluster(cluster_id: str):
    return DatabricksSession.builder.remote(
        host=server_hostname, cluster_id=cluster_id
    ).getOrCreate()


with tab_a:
    iframe_source = st.text_input(
        "Specify iframe source:",
        placeholder="https://adb-984752964297111.11.azuredatabricks.net/embed/dashboardsv3/01efe9b7bd801f99a084f79a00bf51d9?o=984752964297111",
        help="Copy a iframe source link [cluster ID](https://docs.databricks.com/en/workspace/workspace-details.html#cluster-url-and-id) to embed.",
    )

    if iframe_source:
        components.iframe(
        src=iframe_source,
        width=700,
        height=600,
        scrolling=True
)

with tab_b:
    st.code(
        """
        iframe_source = st.text_input(
        "Specify iframe source:",
        placeholder="https://adb-984752964297111.11.azuredatabricks.net/embed/dashboardsv3/01efe9b7bd801f99a084f79a00bf51d9?o=984752964297111",
        help="Copy a iframe source link [cluster ID](https://docs.databricks.com/en/workspace/workspace-details.html#cluster-url-and-id) to embed.",
    )

    if iframe_source:
        components.iframe(
        src=iframe_source,
        width=700,
        height=600,
        scrolling=True
)

        """
    )

with tab_c:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
                    **Permissions (app service principal)**
                    * `CAN ATTACH TO` permission on the cluster
                    """)
    with col2:
        st.markdown("""
                    **Databricks resources**
                    * All-purpose compute
                    """)
    with col3:
        st.markdown("""
                    **Dependencies**
                    * [Databricks Connect](https://pypi.org/project/databricks-connect/) - `databricks-connect`
                    * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
                    """)






