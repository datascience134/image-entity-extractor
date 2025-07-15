import base64
import streamlit as st
from openai import AzureOpenAI

st.title("Vision-Based Entity Extractor")

# Load secrets
AZUREOPENAI_ENDPOINT = st.secrets["AZUREOPENAI_ENDPOINT"]
AZUREOPENAI_API_KEY = st.secrets["AZUREOPENAI_API_KEY"]

# Show confirmation message
st.success("Loaded endpoint and API key successfully!")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZUREOPENAI_ENDPOINT,
    api_key=AZUREOPENAI_API_KEY,
    api_version="2024-02-01"
)

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Show uploaded image
    st.image(uploaded_file)

    # Read and encode image to base64
    image_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(image_bytes).decode('utf-8')

    st.success("Image successfully converted to base64!")

    # Define your prompt
    prompt = (
        "Extract the total amount paid, shop name, and receipt date from this receipt. "
        "Return as JSON. If missing, use ''. Date should be in DD/MM/YYYY."
    )

    # Button to trigger inference
    if st.button("Run Inference"):
        with st.spinner("Running inference..."):
            try:
                response_text = client.chat.completions.create(
                    model="gpt-4.1",  # your deployed model name
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ],
                        }
                    ],
                    max_tokens=500,
                )
                answer = response_text.choices[0].message.content
                st.subheader("Extracted Information")
                st.code(answer)
            except Exception as e:
                st.error(f"Error during inference: {e}")
