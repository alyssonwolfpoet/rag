import streamlit as st
import requests

# Configuração do Streamlit
st.title("Assistente Técnico")
st.header("Pesquisa de Documentos")

# Barra lateral para enviar PDFs
st.sidebar.title("Enviar PDF")
uploaded_file = st.sidebar.file_uploader("Selecione um PDF", type=["pdf"])

# Chat
chat_history = []

def send_message(query):
    response = requests.post("http://localhost:8080/ask_pdf", json={"query": query})
    if response.status_code == 200:
        chat_history.append({"user": query, "assistant": response.json()["answer"]})
        st.session_state.chat_history = chat_history
    else:
        st.error("Erro ao enviar mensagem")

def display_chat_history():
    for message in chat_history:
        st.write(f"**Você:** {message['user']}")
        st.write(f"**Assistente:** {message['assistant']}")

if uploaded_file is not None:
    # Enviar o PDF para o servidor
    response = requests.post("http://localhost:8080/pdf", files={"files": uploaded_file})
    if response.status_code == 200:
        st.sidebar.success("PDF enviado com sucesso!")
    else:
        st.sidebar.error("Erro ao enviar PDF")

query = st.text_input("Digite sua pergunta:")
if st.button("Enviar"):
    send_message(query)

st.subheader("Histórico de Conversa")
display_chat_history()