from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# ─── SUPABASE ULANISH ─────────────────────────────────────────────────────────
SUPABASE_URL = "https://rsoulilpsujserfurlrzp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJzb3VsaWxwc3Vqc2VyZnVscnpwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0ODg1MTAsImV4cCI6MjA4NzA2NDUxMH0.q1RD6wghenUFiOcycHJ0KMHtF41ujItv5YwaAbTdsAM"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

TABLE_URL = f"{SUPABASE_URL}/rest/v1/olchash_vositalari"

# ─── BARCHA RO'YXATNI OLISH ───────────────────────────────────────────────────
@app.route('/api/instruments', methods=['GET'])
def get_instruments():
    try:
        res = requests.get(TABLE_URL, headers=HEADERS, params={"order": "sana.desc"})
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── BITTA O'LCHASH VOSITASINI OLISH ─────────────────────────────────────────
@app.route('/api/instruments/<id>', methods=['GET'])
def get_instrument(id):
    try:
        res = requests.get(TABLE_URL, headers=HEADERS, params={"id": f"eq.{id}"})
        data = res.json()
        if data:
            return jsonify(data[0]), 200
        return jsonify({'error': 'Topilmadi'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── YANGI O'LCHASH VOSITASI QO'SHISH ────────────────────────────────────────
@app.route('/api/instruments', methods=['POST'])
def add_instrument():
    try:
        data = request.get_json()
        h = {**HEADERS, "Prefer": "return=representation"}
        res = requests.post(TABLE_URL, headers=h, json=data)
        result = res.json()
        return jsonify(result[0] if isinstance(result, list) else result), res.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── O'LCHASH VOSITASINI O'CHIRISH ───────────────────────────────────────────
@app.route('/api/instruments/<id>', methods=['DELETE'])
def delete_instrument(id):
    try:
        res = requests.delete(TABLE_URL, headers=HEADERS, params={"id": f"eq.{id}"})
        return jsonify({'message': "O'chirildi"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ─── ISHGA TUSHIRISH ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
