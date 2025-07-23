from flask import Flask, request, render_template
import csv
import os

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
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_message():
    # Get data from the POST request
    device_id = request.json.get('device_id')
    phone_number = request.json.get('phone_number')
    message_type = request.json.get('message_type')
    timestamp = request.json.get('timestamp')

    # Write data to CSV
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([device_id, phone_number, message_type, timestamp])

    return {"status": "success"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
