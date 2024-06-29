from flask import Flask, request, jsonify, render_template, redirect, url_for
from supabase import create_client, Client
import logging
import pickle
import pandas as pd
from datetime import datetime
import requests
import numpy as np

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import Model
loaded_model = pickle.load(open('trained_model.sav', 'rb'))
loaded_scaler = pickle.load(open('scaler.sav', 'rb'))

ESP32_URL = 'http://192.168.84.159'

# Supabase configuration
supabase_url = 'https://jchndtdkbmzgppgxpfio.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpjaG5kdGRrYm16Z3BwZ3hwZmlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY4NzQ3MDQsImV4cCI6MjAzMjQ1MDcwNH0.WsZKLhMuQNy6ghqX_-kJdAmMobzAmb1wDO4POjNsFOI'
supabase: Client = create_client(supabase_url, supabase_key)

@app.route("/", methods=['GET'])
def homepage():
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error("Error rendering homepage: %s", e)
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route("/login", methods=['POST'])
def login():
    try:
        user = request.form.get('username')
        pwd = request.form.get('password')

        if not (user and pwd):
            return jsonify({'status': 'error', 'message': 'Incomplete data'}), 400

        response = supabase.table('user').select('username', 'password').execute()
        
        berhasil = False
        for row in response.data:
            if row['username'] == user and row['password'] == pwd:
                berhasil = True
                break
        
        if berhasil:
            return redirect(url_for('chart1'))
        else:
            return jsonify({'status': 'error', 'message': 'Username atau password salah'}), 401

    except Exception as e:
        app.logger.error("Login error: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/data", methods=['GET'])
def get_data():
    try:
        response = supabase.table('data').select('id_micro, ph, suhu, lembab').execute()
        print("Database Berhasil Di Akses")  # Debugging response

        if hasattr(response, 'error') and response.error:
            return jsonify({'status': 'error', 'message': response.error['message']}), 500

        rows = response.data
        print("Rows:", len(rows))  # Debugging rows

        data = {
            "id_micro": [row['id_micro'] for row in rows],
            "ph": [row['ph'] for row in rows],
            "suhu": [row['suhu'] for row in rows],
            "lembab": [row['lembab'] for row in rows]
        }
        
        # Create DataFrame
        new_data_df = pd.DataFrame(data)
        
        # Process DataFrame
        dfdrop = new_data_df.drop(columns=['id_micro'])
        dftemp = dfdrop.rename(columns={'suhu': 'Temperature'})
        dfsoil = dftemp.rename(columns={'lembab': 'Soil Moisture'})
        
        # Scale data
        scaled_new_data = loaded_scaler.transform(dfsoil)
        
        # Predict
        prediction = loaded_model.predict(scaled_new_data)
        print(prediction)
        
        # Get last prediction
        last_prediction = prediction[-1]
        print("Last Prediction:", last_prediction)

        # Save last prediction to Supabase
        save_prediction_to_supabase(last_prediction)

        # Prepare response data
        response_data = {
            "data": data,
            "prediction": prediction.tolist(),  # Convert prediction to list for JSON serialization
            "last_prediction": last_prediction
        }
        
        return jsonify(data)
    except Exception as e:
        app.logger.error("Data retrieval error: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

def save_prediction_to_supabase(last_prediction):
    try:
        # Convert int64 to int if necessary
        if isinstance(last_prediction, np.int64):
            last_prediction = int(last_prediction)

        # Prepare data to insert
        data_to_insert = {
            "keterangan": last_prediction
        }

        # Insert data into Supabase
        response = supabase.table('Hasil').insert(data_to_insert).execute()
        
        if hasattr(response, 'error') and response.error:
            app.logger.error("Error saving prediction to Supabase: %s", response.error)
        else:
            app.logger.debug("Successfully saved prediction to Supabase: %s", response.data)

    except Exception as e:
        app.logger.error("Error in save_prediction_to_supabase: %s", e)




@app.route("/1")
def chart1():
    try:
        return render_template('chart1.html')
    except Exception as e:
        app.logger.error("Error rendering chart1: %s", e)
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500

@app.route("/2")
def chart2():
    try:
        return render_template('chart2.html')
    except Exception as e:
        app.logger.error("Error rendering chart2: %s", e)
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500


@app.route("/test-connection", methods=['GET'])
def test_connection():
    try:
        response = supabase.table('data').select('id_micro').limit(1).execute()
        app.logger.debug("Response from Supabase: %s", response)

        if 'data' not in response:
            return jsonify({'status': 'error', 'message': 'Error testing connection'}), 500
        
        return jsonify({'status': 'success', 'message': 'Connection successful', 'data': response['data']}), 200
    except Exception as e:
        app.logger.error("Test connection error: %s", e)
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
