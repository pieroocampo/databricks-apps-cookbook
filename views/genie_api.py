import streamlit as st
import requests
import time
import pandas as pd

st.title("Databricks Genie Chat")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    workspace_instance_name = st.text_input("Workspace Instance Name")
    authentication_token = st.text_input("Authentication Token", type='password')
    space_id = st.text_input("Genie Space ID")

# Headers for API requests
headers = {
    'Authorization': f'Bearer {authentication_token}'
}

# Function to start a conversation
def start_conversation(space_id, question):
    url = f'https://{workspace_instance_name}/api/2.0/genie/spaces/{space_id}/start-conversation'
    response = requests.post(url, json={'content': question}, headers=headers)
    return response.json()

# Function to get conversation message
def get_conversation_message(space_id, conversation_id, message_id):
    url = f'https://{workspace_instance_name}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}'
    response = requests.get(url, headers=headers)
    return response.json()

# Function to get query result
def get_query_result(space_id, conversation_id, message_id):
    url = f'https://{workspace_instance_name}/api/2.0/genie/spaces/{space_id}/conversations/{conversation_id}/messages/{message_id}/query-result'
    response = requests.get(url, headers=headers)
    return response.json()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message:
            st.dataframe(message["data"])

# Chat input
if prompt := st.chat_input("Ask Genie a question"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if workspace_instance_name and authentication_token and space_id:
            try:
                start_response = start_conversation(space_id, prompt)
                conversation_id = start_response['conversation_id']
                message_id = start_response['message_id']

                while True:
                    message_response = get_conversation_message(space_id, conversation_id, message_id)
                    status = message_response['status']

                    if status == 'COMPLETED':
                        result_response = get_query_result(space_id, conversation_id, message_id)
                        rows = [[c['str'] for c in r['values']] for r in result_response['result']['data_array']]
                        columns = [c['name'] for c in result_response['manifest']['schema']['columns']]
                        df = pd.DataFrame(rows, columns=columns)
                        
                        message_placeholder.markdown("Here's the result of your query:")
                        st.dataframe(df)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": "Here's the result of your query:", "data": df})
                        break
                    elif status == 'FAILED':
                        message_placeholder.error('Query failed.')
                        st.session_state.messages.append({"role": "assistant", "content": "Query failed."})
                        break
                    time.sleep(2)
            except Exception as e:
                message_placeholder.error(f"An error occurred: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"An error occurred: {str(e)}"})
        else:
            message_placeholder.error('Please fill in all configuration fields in the sidebar.')
            st.session_state.messages.append({"role": "assistant", "content": "Please fill in all configuration fields in the sidebar."})
