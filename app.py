from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data["message"].lower()

    conn = get_db()
    cursor = conn.cursor()

    # 🔹 1. DATABASE KONTROL
    cursor.execute("""
        SELECT threat_type FROM threats
        WHERE ? LIKE '%' || keyword || '%'
    """, (user_input,))

    result = cursor.fetchone()

    if result:
        threat_type = result[0]

        cursor.execute("""
            SELECT response FROM responses
            WHERE threat_type=?
        """, (threat_type,))

        reply = cursor.fetchone()

        return jsonify({
            "reply": reply[0],
            "severity": "HIGH"
        })

    # 🔹 2. PATTERN ANALYSIS (fallback)
    if "failed" in user_input and "login" in user_input:
        return jsonify({
            "reply": "⚠ Brute force pattern detected",
            "severity": "HIGH"
        })

    if "select" in user_input or "drop" in user_input:
        return jsonify({
            "reply": "🚨 Possible SQL Injection",
            "severity": "CRITICAL"
        })

    if "<script>" in user_input:
        return jsonify({
            "reply": "⚠ XSS attack detected",
            "severity": "MEDIUM"
        })

    if "flood" in user_input or "traffic spike" in user_input:
        return jsonify({
            "reply": "🚨 Possible DDoS",
            "severity": "CRITICAL"
        })

    # 🔹 3. DEFAULT (EN ÖNEMLİ)
    return jsonify({
        "reply": "⚠ No threat detected",
        "severity": "LOW"
    })


if __name__ == "__main__":
    app.run(debug=True)