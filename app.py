from flask import Flask, request, jsonify
from supabase import create_client, Client
from datetime import datetime
import os

# Load Supabase credentials from environment variables
SUPABASE_URL = os.environ.get("https://xhlyzfuidcgaviwimyll.supabase.co/")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhobHl6ZnVpZGNnYXZpd2lteWxsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5MjQyNjMsImV4cCI6MjA1OTUwMDI2M30.GukI9P58O0K_tZhk99upaZ7Th5TT8HVHGGUirt17NEw")

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files and not request.data:
        return jsonify({'error': 'No image provided'}), 400

    # Generate a timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.jpg"

    # Upload to Supabase storage
    try:
        image_data = request.data
        res = supabase.storage.from_('esp32-uploads').upload(
            path=filename,
            file=image_data,
            file_options={"content-type": "image/jpeg"},
            upsert=True
        )
        return jsonify({'message': 'Image uploaded', 'filename': filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Landslide ESP32 Cloud Backend is Running", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
