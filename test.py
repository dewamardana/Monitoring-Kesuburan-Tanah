import requests

# URL ESP32, ganti dengan IP address ESP32 Anda
url = "http://192.168.84,159/data"

# Data yang akan dikirim, misalnya data sensor
data = {
    'temperature': 25.5,
    'humidity': 60
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Data berhasil dikirim")
    else:
        print(f"Gagal mengirim data, status code: {response.status_code}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
