#!/usr/bin/env python
# coding: utf-8

# In[1]:

import base64
import streamlit as st

from openai import AzureOpenAI

st.title("Vision-Based Entity Extractor")


AZUREOPENAI_ENDPOINT = st.secrets["AZUREOPENAI_ENDPOINT"]
AZUREOPENAI_API_KEY = st.secrets["AZUREOPENAI_API_KEY"]

st.write("Loaded endpoint and API key successfully!")

client = AzureOpenAI(
  azure_endpoint = AZUREOPENAI_ENDPOINT,
  api_key=AZUREOPENAI_API_KEY,
  api_version="2024-02-01"
)

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file)
    image_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
    st.success("Image successfully converted to base64!")

