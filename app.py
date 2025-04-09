from flask import Flask, request, jsonify
from supabase import create_client, Client
import requests
import mimetypes
import uuid
from datetime import datetime

app = Flask(__name__)

# 🔑 Replace these with your Supabase keys
SUPABASE_URL = "https://xhlyzfuidcgaviwimyll.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhobHl6ZnVpZGNnYXZpd2lteWxsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5MjQyNjMsImV4cCI6MjA1OTUwMDI2M30.GukI9P58O0K_tZhk99upaZ7Th5TT8HVHGGUirt17NEw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧠 Upload sensor data to Supabase table
@app.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.get_json()
    soil = data.get('soil')
    gyro = data.get('gyro')

    result = supabase.table("sensor_data").insert({
        "soil": soil,
        "gyro": gyro,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return jsonify({"status": "Sensor data uploaded", "result": result.data}), 201

# 📸 Upload image to Supabase Storage
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    filename = str(uuid.uuid4()) + "_" + image_file.filename
    content_type = mimetypes.guess_type(filename)[0]

    image_data = image_file.read()
    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": content_type,
    }

    url = f"{SUPABASE_URL}/storage/v1/object/images/{filename}"
    response = requests.put(url, headers=headers, data=image_data)

    if response.status_code in [200, 201]:
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/images/{filename}"
        return jsonify({"message": "Image uploaded", "url": public_url}), 201
    else:
        return jsonify({"error": "Upload failed", "details": response.text}), 500

# 🌐 Optional: View latest 10 readings
@app.route('/latest', methods=['GET'])
def get_latest():
    data = supabase.table("sensor_data").select("*").order("timestamp", desc=True).limit(10).execute()
    return jsonify(data.data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
