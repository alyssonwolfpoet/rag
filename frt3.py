import streamlit as st
import requests

st.title("Conversa com o Assistente Técnico")

chat_history = []

def update_chat_history(message):
    chat_history.append(message)
    st.write("Histórico de conversa:")
    for message in chat_history:
        st.write(f"  - {message}")

def send_message(query):
    response = requests.post("http://localhost:8080/ask_pdf", json={"query": query})
    result = response.json()
    update_chat_history(f"Você: {query}")
    update_chat_history(f"Assistente: {result['answer']}")
    for source in result["sources"]:
        update_chat_history(f"Fonte: {source['source']}")

query = st.text_input("Digite sua pergunta ou consulta")

if st.button("Enviar"):
    send_message(query)

st.write("Histórico de conversa:")
for message in chat_history:
    st.write(f"  - {message}")