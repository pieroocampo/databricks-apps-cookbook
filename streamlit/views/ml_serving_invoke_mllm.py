import io
import base64
import streamlit as st
from PIL import Image
from typing import Dict
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()


st.header(body="AI / ML", divider=True)
st.subheader("Invoke a multi-modal LLM")
st.write(
    "Upload an image and provide a prompt for multi-modal inference, e.g., using Llama 3.2."
)

tab1, tab2, tab3 = st.tabs(["**Try it**", "**Code snippet**", "**Requirements**"])


def pillow_image_to_base64_string(img):
    """Convert a Pillow image to a base64-encoded string for API transmission."""
    buffered = io.BytesIO()
    img.convert("RGB").save(buffered, format="JPEG")

    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def chat_with_mllm(endpoint_name, prompt, image, messages=None) -> tuple[str, Dict]:
    """
    Chat with a multi-modal LLM using Mosaic AI Model Serving.
    
    This function sends the prompt and image(s) to a deployed Llama 3.2 endpoint
    using Databricks SDK.
    """
    
    request_data = {
        "user_query": prompt,
        "image": pillow_image_to_base64_string(image)
    }
    
    response = w.serving_endpoints.query(
        name=endpoint_name,
        dataframe_records=[request_data]
    )
    
    generated_text = ""
    if response.get("predictions"):
        generated_text = response.predictions[0]
    
    # Update conversation history
    if not messages:
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
    else:
        messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})
    
    messages.append({"role": "assistant", "content": [{"type": "text", "text": generated_text}]})
    
    return generated_text, messages


with tab1:
    endpoints = w.serving_endpoints.list()
    endpoint_names = [endpoint.name for endpoint in endpoints]

    selected_model = st.selectbox(
        "Select a model served by Model Serving", endpoint_names
    )

    uploaded_file = st.file_uploader("Select an image (JPG, JPEG, or PNG)", type=["jpg", "jpeg", "png"])

    prompt = st.text_area(
        "Enter your prompt:", 
        placeholder="Describe or ask something about the image...",
        value="Describe the images as an alternative text",
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image")

    if st.button("Invoke LLM"):
        if uploaded_file:
            with st.spinner("Processing..."):
                generated_text, conversation, _ = chat_with_mllm(
                    endpoint_name=selected_model,
                    prompt=prompt,
                    image=image,
                )
            
            st.write(generated_text)
        else:
            st.error("Please upload an image to proceed.")


with tab2:
    st.code("""
    import streamlit as st
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    openai_client = w.serving_endpoints.get_open_ai_client()

    EMBEDDING_MODEL_ENDPOINT_NAME = "databricks-gte-large-en"


    def get_embeddings(text):
        try:
            response = openai_client.embeddings.create(
                model=EMBEDDING_MODEL_ENDPOINT_NAME, input=text
            )
            return response.data[0].embedding
        except Exception as e:
            st.text(f"Error generating embeddings: {e}")


    def run_vector_search(prompt: str) -> str:
        prompt_vector = get_embeddings(prompt)
        if prompt_vector is None or isinstance(prompt_vector, str):
            return f"Failed to generate embeddings: {prompt_vector}"

        columns_to_fetch = [col.strip() for col in columns.split(",") if col.strip()]

        try:
            query_result = w.vector_search_indexes.query_index(
                index_name=index_name,
                columns=columns_to_fetch,
                query_vector=prompt_vector,
                num_results=3,
            )
            return query_result.result.data_array
        except Exception as e:
            return f"Error during vector search: {e}"


    index_name = st.text_input(
        label="Unity Catalog Vector search index:",
        placeholder="catalog.schema.index-name",
    )

    columns = st.text_input(
        label="Columns to retrieve (comma-separated):",
        placeholder="url, name",
        help="Enter one or more column names present in the vector search index, separated by commas. E.g. id, text, url.",
    )

    text_input = st.text_input(
        label="Enter your search query:",
        placeholder="What is Databricks?",
        key="search_query_key",
    )

    if st.button("Run vector search"):
        result = run_vector_search(text_input)
        st.write("Search results:")
        st.write(result)
    """)

with tab3:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
                    **Permissions (app service principal)**
                    * `CAN QUERY` on the model serving endpoint
                    """)
    with col2:
        st.markdown("""
                    **Databricks resources**
                    * Model serving endpoint
                    """)
    with col3:
        st.markdown("""
                    **Dependencies**
                    * [Databricks SDK for Python](https://pypi.org/project/databricks-sdk/) - `databricks-sdk`
                    * [Streamlit](https://pypi.org/project/streamlit/) - `streamlit`
                    """)
