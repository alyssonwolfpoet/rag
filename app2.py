from flask import Flask, request, jsonify
from langchain_community import (
    Ollama,
    Chroma,
    RecursiveCharacterTextSplitter,
    FastEmbedEmbeddings,
    PDFPlumberLoader,
)
from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
from langchain.prompts import PromptTemplate

app = Flask(__name__)

FOLDER_PATH = "db"
LLM_MODEL = "llama3"

# Configurações globais
llm = Ollama(model=LLM_MODEL)
embedding = FastEmbedEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

# Prompt template
prompt_template = PromptTemplate.from_template(
    """ 
    <s>[INST] Você é um assistente técnico bom em pesquisar documentos. Se você não tiver uma resposta com base nas informações fornecidasno Contexto, diga-o nada foi encontrado.[/INST] 
    [INST] {input}
        Contexto: {context}
        Responder: 
    [/INST]
"""
)

# Chains
document_chain = create_stuff_documents_chain(llm, prompt_template)

def create_retrieval_chain(query):
    vector_store = Chroma(persist_directory=FOLDER_PATH, embedding_function=embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 1, "score_threshold": 0.1},
    )
    chain = create_retrieval_chain(retriever, document_chain)
    return chain

@app.route("/ai", methods=["POST"])
def ai_post():
    query = request.get_json()["query"]
    response = llm.invoke(query)
    return jsonify({"answer": response})

@app.route("/ask_pdf", methods=["POST"])
def ask_pdf_post():
    query = request.get_json()["query"]
    chain = create_retrieval_chain(query)
    result = chain.invoke({"input": query})
    sources = [{"source": doc.metadata["source"], "page_content": doc.page_content} for doc in result["context"]]
    return jsonify({"answer": result["answer"], "sources": sources})

@app.route("/pdf", methods=["POST"])
def pdf_post():
    file = request.files["file"]
    file_name = file.filename
    save_file = "pdf/" + file_name
    file.save(save_file)
    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    chunks = text_splitter.split_documents(docs)
    vector_store = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=FOLDER_PATH)
    vector_store.persist()
    return jsonify({
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    })

def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    start_app()