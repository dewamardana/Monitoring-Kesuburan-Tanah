from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pkb'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306  # Sesuaikan dengan port MySQL Anda

mysql = MySQL(app)

# @app.route("/")
# def hello():
#     return "Hello, World!"

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
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO data (id_micro, ph, suhu, lembab) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_micro, ph, suhu, lembab))
            mysql.connection.commit()
            cursor.close()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/data", methods=['GET'])
def get_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id_micro, ph, suhu, lembab FROM data")
    rows = cursor.fetchall()
    cursor.close()

    data = {
        "id_micro": [row[0] for row in rows],
        "ph": [row[1] for row in rows],
        "suhu": [row[2] for row in rows],
        "lembab": [row[3] for row in rows]
    }

    return jsonify(data)

@app.route("/1")
def chart1():
    return render_template('chart1.html')

@app.route("/2")
def chart2():
    return render_template('chart2.html')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
     app.run(debug=True)