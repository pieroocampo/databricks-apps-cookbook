import streamlit as st
import streamlit.components.v1 as components

st.header("Data Visualization", divider=True)
st.subheader("AI/BI Dashboard")
st.write(
    """
    This recipe uses [Databricks AI/BI](https://www.databricks.com/product/ai-bi) to embed a previously created dashboard into a Databricks App. 
    """
)
tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])


with tab_a:
    iframe_source = st.text_input(
        "Specify iframe source:",
        placeholder="https://workspace.azuredatabricks.net/embed/dashboardsv3/dashboard-id",
        help="Copy a iframe source link to embed.",
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
        iframe_source = "https://workspace.azuredatabricks.net/embed/dashboardsv3/dashboard-id"
    )

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
                    * Access to dashboard
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






