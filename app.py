#!/usr/bin/env python
# coding: utf-8

# In[1]:

import base64
import streamlit as st

st.title("Vision-Based Entity Extractor")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file)
    image_bytes = uploaded_file.read()
    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
    st.success("Image successfully converted to base64!")

