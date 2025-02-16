import streamlit as st
import requests
import time
import pandas as pd
from databricks.sdk.core import Config


st.header("Genie", divider=True)
st.subheader("Converse with your data")
st.write(
    """
    This app uses [Databricks AI/BI Genie](https://www.databricks.com/product/ai-bi) to let users ask questions about your data for instant insights.
    """
)

cfg = Config()

tab_a, tab_b, tab_c = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])

with tab_a:
    genie_space_id = st.text_input("Genie Space ID")
    authentication_token = st.text_input("Authentication Token", type="password")

    headers = {
        "Authorization": f"Bearer {authentication_token}"
    }

    # Function definitions (start_conversation, get_conversation_message, get_query_result) go here

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "data" in message:
                st.dataframe(message["data"])

    if prompt := st.chat_input("Ask Genie a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if cfg.host and genie_space_id and authentication_token:
                try:
                    # API interaction code goes here
                    pass
                except Exception as e:
                    message_placeholder.error(f"An error occurred: {str(e)}")
                    st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})
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
                    * [Requests](https://pypi.org/project/requests/) - `requests`
                    * [Databricks SDK](https://pypi.org/project/databricks-sdk/) - `databricks-sdk`
                    * [Pandas](https://pypi.org/project/pandas/) - `pandas`
                    """)
