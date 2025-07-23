
import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Path to store the CSV log file
csv_file = "logs.csv"

# Create the CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Device ID", "Phone Number", "Message Type", "Timestamp"])

@app.route('/')
def index():
    # Read logs from CSV file
    logs = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            logs = list(reader)
    
    return render_template('logs.html', logs=logs)

@app.route('/log', methods=['POST'])
def log_message():
    # Get the incoming JSON data
    data = request.json
    print("[📥 Received JSON]", data)
    
    # Extract specific fields if they exist
    device_id = data.get('device_id') if data else None
    phone_number = data.get('phone_number') if data else None
    message_type = data.get('message_type') if data else None
    timestamp = data.get('timestamp') if data else None

    # Write data to CSV if we have the required fields
    if device_id or phone_number or message_type or timestamp:
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([device_id, phone_number, message_type, timestamp])

    return {"status": "success"}, 200

@app.route('/upload')
def upload_logs():
    # Placeholder for Google Drive upload functionality
    return {"status": "Upload functionality coming soon!"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
