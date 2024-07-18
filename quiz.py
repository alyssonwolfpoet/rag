import streamlit as st
import requests

st.title("Document Search and Answering System")

query_input = st.text_input("Enter your query:")

pdf_upload = st.file_uploader("Upload PDF files:", accept_multiple_files=True)

if st.button("Search"):
    if query_input:
        response = requests.post("http://localhost:8080/ask_pdf", json={"query": query_input})
        result = response.json()
        st.write("Answer:", result["answer"])
        st.write("Sources:")
        for source in result["sources"]:
            st.write(f"  - {source['source']}: {source['page_content']}")

if pdf_upload:
    files = [{"filename": file.name, "file": file} for file in pdf_upload]
    response = requests.post("http://localhost:8080/pdf", files={"files": files})
    result = response.json()
    st.write("Upload result:", result)