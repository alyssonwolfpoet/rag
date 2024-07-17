import streamlit as st
import json

# Carregue o JSON
with open('quiz.json') as f:
    quiz_data = json.load(f)

# Crie uma lista para armazenar as respostas do usuário
user_answers = []

# Crie um título para o quiz
st.title(quiz_data['title'])
st.write("")

# Percorra as perguntas do quiz
for i, question in enumerate(quiz_data['questions']):
    # Crie uma seção para a pergunta
    with st.expander(question['question']):
        # Crie uma pergunta com opções
        options = question['options']
        answer = st.selectbox('Selecione uma opção', options, key=f"question_{i}")

        # Armazene a resposta do usuário
        user_answers.append(answer)

        # Mostra a explicação da pergunta
        st.write(question['explanation'])
        st.write("")

# Mostra o resultado do quiz
st.write("")
st.write("Resultado:")
correct_answers = [question['options'][int(question['correct'])] for question in quiz_data['questions']]
score = sum([a == b for a, b in zip(user_answers, correct_answers)])
st.write(f'Você acertou {score} de {len(quiz_data["questions"])} perguntas!')