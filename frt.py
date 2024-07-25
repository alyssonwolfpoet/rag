import streamlit as st
import requests

# Configuração do Streamlit
st.title("Assistente Técnico")
st.header("Pesquisa de Documentos")

# Barra lateral para enviar PDFs
st.sidebar.title("Enviar PDF")
uploaded_file = st.sidebar.file_uploader("Selecione um PDF", type=["pdf"])

if uploaded_file is not None:
    # Enviar o PDF para o servidor
    response = requests.post("http://localhost:8080/pdf", files={"files": uploaded_file})
    if response.status_code == 200:
        st.sidebar.success("PDF enviado com sucesso!")
    else:
        st.sidebar.error("Erro ao enviar PDF")

# Rota /ask_pdf
st.subheader("Perguntar sobre um PDF")
ask_query = st.text_input("Digite sua pergunta:")
if st.button("Perguntar"):
    response = requests.post("http://localhost:8080/ask_pdf", json={"query": ask_query})
    if response.status_code == 200:
        st.write(response.json()["answer"])
    else:
        st.error("Erro ao perguntar")