import streamlit as st
from databricks.sdk.core import Config
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.dashboards import GenieMessage
import pandas as pd

w = WorkspaceClient()


st.header("Genie", divider=True)
st.subheader("Converse with your data")
st.write(
    """
    This app uses [Genie](https://www.databricks.com/product/ai-bi) [API](https://docs.databricks.com/api/workspace/genie) to let users ask questions about your data for instant insights.
    """
)
st.warning("Public Preview")

cfg = Config()

tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

with tab_a:
    genie_space_id = st.text_input("Genie Space ID")

    message_placeholder = st.empty()

    def display_table(statement_id: str):
        statement = w.statement_execution.get_statement(statement_id)
        data = pd.DataFrame(statement.result.data_array, columns=[i.name for i in statement.manifest.schema.columns])
        st.dataframe(data)

    def process_genie_response(response: GenieMessage):
        if response.attachments:
            for i in response.attachments:
                if i.text:
                    reply = i.text.content
                    message_placeholder.markdown(reply)
                    st.session_state["messages"].append({"role": "assistant", "content": reply})
                if i.query:
                    reply = i.query.description
                    message_placeholder.markdown(reply)
                    display_table(i.query.statement_id)
                    st.session_state["messages"].append({"role": "assistant", "content": reply})
                    with st.expander("Show generated code"):
                        st.code(i.query.query, language="sql", wrap_lines=True)


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "data" in message:
                st.dataframe(message["data"])

    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if genie_space_id:
                response = w.genie.start_conversation_and_wait(genie_space_id, prompt)
                process_genie_response(response)
            else:
                message_placeholder.error('Please fill in all configuration fields in the sidebar.')
                st.session_state.messages.append({"role": "assistant", "content": "Please fill in all configuration fields in the sidebar."})

with tab_b:
    st.code(
        """
        import streamlit as st
        import requests
        import pandas as pd
        from databricks.sdk.core import Config

        # Configuration
        cfg = Config()
        genie_space_id = "your_space_id"
        authentication_token = "your_auth_token"

        headers = {
            'Authorization': f'Bearer {authentication_token}'
        }

        def start_conversation(genie_space_id, question):
            url = f'{cfg.host}/api/2.0/genie/spaces/{genie_space_id}/start-conversation'
            response = requests.post(url, json={'content': question}, headers=headers)
            return response.json()

        # Chat
        prompt = st.chat_input("Ask Genie a question")
        if prompt:
            start_response = start_conversation(genie_space_id, prompt)
            # Process the response and display results
        """
    )

with tab_c:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
                    **Permissions**
                    * Genie space
                    * API access token
                    """)
    with col2:
        st.markdown("""
                    **Databricks resources**
                    * AI/BI Genie Conversations API
                    """)
    with col3:
        st.markdown("""
                    **Dependencies**
                    * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
                    * [Databricks SDK](https://pypi.org/project/databricks-sdk/) - `databricks-sdk`
                    * [Pandas](https://pypi.org/project/pandas/) - `pandas`
                    """)
