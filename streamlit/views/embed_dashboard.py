import streamlit as st
import streamlit.components.v1 as components

st.header("Data Visualization", divider=True)
st.subheader("AI/BI Dashboard")
st.write(
    """
    This recipe uses [Databricks AI/BI](https://www.databricks.com/product/ai-bi) to embed a dashboard into a Databricks App. 
    """
)
tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])


with tab_a:
    iframe_source = st.text_input(
        "Embed the dashboard:",
        placeholder="https://dbc-f0e9b24f-3d49.cloud.databricks.com/embed/dashboardsv3/01eff8112e9411cd930f0ae0d2c6b63d?o=37581543725667790",
        help="Copy and paste the URL from the dashboard UI Share -> Embed iframe.",
    )

    if iframe_source:
        components.iframe(src=iframe_source, width=700, height=600, scrolling=True)

with tab_b:
    st.code(
        """
        import streamlit.components.v1 as components
        
        iframe_source = "https://workspace.azuredatabricks.net/embed/dashboardsv3/dashboard-id"

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
                    * `CAN VIEW` permission on the dashboard
                    """)
    with col2:
        st.markdown("""
                    **Databricks resources**
                    * SQL Warehouse
                    """)
    with col3:
        st.markdown("""
                    **Dependencies**
                    * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
                    """)

    st.warning(
        "A workspace admin needs to enable dashboard embedding in the Security settings of your Databricks workspace for specific domains (e.g., databricksapps.com) or all domains for this sample to work.",
        icon="⚠️",
    )
