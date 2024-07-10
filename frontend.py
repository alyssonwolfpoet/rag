# frontend.py

import streamlit as st
import requests

# URL base do servidor Flask
BASE_URL = "http://localhost:8080"

def ai_query(query):
    endpoint = f"{BASE_URL}/ai"
    response = requests.post(endpoint, json={"query": query})
    return response.json()

def ask_pdf(query):
    endpoint = f"{BASE_URL}/ask_pdf"
    response = requests.post(endpoint, json={"query": query})
    return response.json()

def upload_pdf(file_path):
    files = {"file": open(file_path, "rb")}
    endpoint = f"{BASE_URL}/pdf"
    response = requests.post(endpoint, files=files)
    return response.json()

def main():
    st.title("Interface para Aplicativo Flask")

    st.header("Consulta de IA")
    query = st.text_area("Digite sua consulta:")
    if st.button("Enviar"):
        if query:
            result = ai_query(query)
            st.write("Resposta:", result["answer"])

    st.header("Consulta em PDF")
    pdf_query = st.text_area("Digite sua consulta em PDF:")
    if st.button("Buscar em PDF"):
        if pdf_query:
            result = ask_pdf(pdf_query)
            st.write("Resposta:", result["answer"])
            st.write("Fontes encontradas:")
            for source in result["sources"]:
                st.write(f"Fonte: {source['source']}")
                st.write(f"Conteúdo da página: {source['page_content']}")

    st.header("Upload de Arquivo PDF")
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
    if st.button("Enviar PDF"):
        if uploaded_file:
            file_path = f"temp.pdf"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            result = upload_pdf(file_path)
            st.write("Status:", result["status"])
            st.write("Arquivo:", result["filename"])
            st.write("Número de documentos:", result["doc_len"])
            st.write("Número de chunks:", result["chunks"])

if __name__ == "__main__":
    main()
