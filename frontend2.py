import streamlit as st
import requests

# Define the base URL for the backend API
BASE_URL = "http://localhost:8080"

# Define functions for each of the API endpoints
def ai_query(query):
    endpoint = f"{BASE_URL}/ai"
    response = requests.post(endpoint, json={"query": query})
    return response.json()

def ask_pdf(query):
    endpoint = f"{BASE_URL}/ask_pdf"
    response = requests.post(endpoint, json={"query": query})
    return response.json()

def upload_pdfs(uploaded_files):
    files_to_send = []
    for uploaded_file in uploaded_files:
        file_path = f"{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        files_to_send.append(("files", open(file_path, "rb")))
    
    endpoint = f"{BASE_URL}/pdf"
    response = requests.post(endpoint, files=dict(files_to_send))
    return response.json()

# Define the main function that runs the Streamlit app
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
                #st.write(f"Conteúdo da página: {source['page_content']}")

    st.header("Upload de Arquivos PDF")
    uploaded_files = st.file_uploader("Escolha um ou mais arquivos PDF", type="pdf", accept_multiple_files=True)
    if st.button("Enviar PDFs"):
        if uploaded_files:
            result = upload_pdfs(uploaded_files)
            st.write("Status:", result["status"])
            st.write("Arquivos:", [file.name for file in uploaded_files])
            st.write("Número de documentos:", result["doc_len"])
            st.write("Número de chunks:", result["chunks"])

if __name__ == "__main__":
    main()