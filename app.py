from flask import Flask, request
from langchain_community.llms import Ollama

app = Flask(__name__)

# llm = Ollama(model="llama3")

# respose = llm.invoke("tell me a cat joke")

# print(respose)

def start_app():
    app.run(host="0.0.0.0", port = 8080 , debug = True)

@app.route("/ai", methods=["POST"])
def aipost():
    print("post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response_answer = "sample response. query: "+ query
    return response_answer

if __name__ == "__main__":
    start_app()
