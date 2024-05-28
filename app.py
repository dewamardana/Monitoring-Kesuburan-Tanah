from flask import Flask, request, jsonify, render_template
from supabase import create_client, Client
import json

app = Flask(__name__)

# Konfigurasi Supabase
supabase_url = 'https://jchndtdkbmzgppgxpfio.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjaG5kdGRrYm16Z3BwZ3hwZmlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4NzQ3MDQsImV4cCI6MjAzMjQ1MDcwNH0.WsZKLhMuQNy6ghqX_-kJdAmMobzAmb1wDO4POjNsFOI'
supabase: Client = create_client(supabase_url, supabase_key)

@app.route("/api/tambah", methods=['POST'])
def api_tambah():
    try:
        # Dapatkan data dari request
        data = request.get_json()
        id_micro = data.get('id')
        ph = data.get('ph')
        suhu = data.get('suhu')
        lembab = data.get('lembab')

        if id_micro and ph and suhu and lembab:
            response = supabase.table('data').insert({
                'id_micro': id_micro,
                'ph': ph,
                'suhu': suhu,
                'lembab': lembab
            }).execute()

            print("Response from Supabase:", response)  # Debugging response

            if hasattr(response, 'error') and response.error:
                return jsonify({'status': 'error', 'message': response.error['message']}), 500

            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/data", methods=['GET'])
def get_data():
    try:
        response = supabase.table('data').select('id_micro, ph, suhu, lembab').execute()
        print("Response from Supabase:", response)  # Debugging response

        if hasattr(response, 'error') and response.error:
            return jsonify({'status': 'error', 'message': response.error['message']}), 500

        rows = response.data
        print("Rows:", rows)  # Debugging rows

        data = {
            "id_micro": [row['id_micro'] for row in rows],
            "ph": [row['ph'] for row in rows],
            "suhu": [row['suhu'] for row in rows],
            "lembab": [row['lembab'] for row in rows]
        }

        print("Data:", data)  # Debugging data

        return jsonify(data)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/1")
def chart1():
    return render_template('chart1.html')

@app.route("/2")
def chart2():
    return render_template('chart2.html')

@app.route("/test-connection", methods=['GET'])
def test_connection():
    try:
        response = supabase.table('data').select('id_micro').limit(1).execute()
        print("Response from Supabase:", response)  # Debugging response

        if hasattr(response, 'error') and response.error:
            return jsonify({'status': 'error', 'message': response.error['message']}), 500
        
        return jsonify({'status': 'success', 'message': 'Connection successful', 'data': response.data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
