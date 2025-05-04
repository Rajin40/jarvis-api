import sys
sys.path.append("D:/python/jervis")
from flask import Flask, request, jsonify, make_response
from backend.British_Brian_Voice import speak  # Jarvis voice
from backend.main_2 import main  # Your ChatBot logic

app = Flask(__name__)

# Manually add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask_jarvis():
    if request.method == "OPTIONS":
        return make_response('', 204)

    data = request.get_json()
    query = data.get("question")

    if not query:
        return jsonify({"error": "No question provided"}), 400

    response = main(query)
    speak(response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

