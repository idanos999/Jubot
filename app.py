from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Server is running!"

@app.route("/transaction", methods=["POST"])
def transaction():

    data = request.json

    print(data)

    return jsonify({
        "success": True,
        "received": data
    })
