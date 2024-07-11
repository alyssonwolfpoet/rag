from flask import Flask, request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

app = Flask(__name__)

folder_path = "db"

cached_llm = Ollama(model="llama3")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2048, chunk_overlap=350, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """
<s>[INST] Você é um assistente técnico especializado em pesquisar informações. Se não encontrar uma resposta com base nas informações fornecidas, diga o que não foi encontrado nehuma informação[/INST]</s>
[INST] {input}
    Contexto: {context}
    Resultado: Pesquisando apenas pelo contexto...
        - Encontre a informação solicitada no contexto e traduzha para português brasileiro se necessário.
        - Se não encontrar nenhuma informação relevante no contexto, informe que não encontrou nada.
        - Pesquisar apenas o conteúdo do contexto e informar se nada for encontrado no contexto.
        - Se o contexto não tiver resultado diga "informação nao encontrada"
[/INST]
"""
)


@app.route("/ai", methods=["POST"])
def aiPost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    json_content = request.json
    query = json_content.get("query")

    # Carregar o vetor de armazenamento
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    # Criar cadeia de busca
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 1,
            "score_threshold": 0.1,
        },
    )

    # Criar cadeia de documentos
    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)

    # Combinar cadeias
    chain = create_retrieval_chain(retriever, document_chain)

    # Invocar a cadeia com a query
    result = chain.invoke({"input": query})

    # Verificar se algum documento foi encontrado
    if result["context"]:
        sources = []
        for doc in result["context"]:
            sources.append({
                "source": doc.metadata["source"],
                "page_content": doc.page_content
            })
        response_answer = {"answer": result["answer"], "sources": sources}
    else:
        response_answer = {"answer": "Não foi encontrado na base de dados.", "sources": []}

    return response_answer

@app.route("/pdf", methods=["POST"])
def pdfPost():
    file = request.files["file"]
    file_name = file.filename
    save_file = "pdf/" + file_name
    file.save(save_file)
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return response


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == "__main__":
    start_app()