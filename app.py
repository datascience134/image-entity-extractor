#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

st.title("Vision-Based Entity Extractor")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file)
    st.success("Now run inference here...")

