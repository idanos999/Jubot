from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchant TEXT,
        amount REAL
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Server is running!"

@app.route("/transaction", methods=["POST"])
def transaction():

    data = request.json

    merchant = data.get("merchant")
    amount = data.get("amount")

    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (merchant, amount) VALUES (?, ?)",
        (merchant, amount)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })

@app.route("/transactions")
def transactions():

    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, merchant, amount FROM transactions"
    )

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)
