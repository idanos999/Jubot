from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        merchant TEXT,
        amount NUMERIC,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cur.close()
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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO transactions (merchant, amount)
        VALUES (%s, %s)
        """,
        (merchant, amount)
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "success": True
    })

@app.route("/transactions")
def transactions():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, merchant, amount, created_at
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "merchant": row[1],
            "amount": float(row[2]),
            "created_at": str(row[3])
        })

    return jsonify(result)
