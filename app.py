from flask import Flask, request
from langchain_community.llms import Ollama

app = Flask(__name__)

cached_llm = Ollama(model="llama3")

def start_app():
    app.run(host="0.0.0.0", port = 8080 , debug = True)

@app.route("/ai", methods=["POST"])
def aipost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    respose = cached_llm.invoke(query)

    print(respose)

    response_answer = {"answer": respose}
    return response_answer

if __name__ == "__main__":
    start_app()
