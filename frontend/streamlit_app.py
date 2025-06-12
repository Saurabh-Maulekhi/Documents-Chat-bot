import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🔍 Document Theme Chatbot")

files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type="pdf")
question = st.text_input("Ask a question:")

if st.button("Upload & Index") and files:
    resp = requests.post(f"{BACKEND_URL}/docs/upload/", files=[("files", f) for f in files])
    st.write(resp.json())

if st.button("Get Answer") and question:
    resp = requests.post(f"{BACKEND_URL}/docs/query/", json={"q": question})
    st.write("**Answer:**", resp.json())
