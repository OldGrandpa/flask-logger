import csv
import datetime
import os
import time
from threading import Thread

import pytz
from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

PAKISTAN_TZ = pytz.timezone('Asia/Karachi')


def get_today_log_filename():
    today = datetime.datetime.now(PAKISTAN_TZ).strftime('%Y-%m-%d')
    return f"log_{today}.txt"


def ensure_log_file():
    filename = get_today_log_filename()
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Device ID", "WhatsApp Type", "Number", "Message Type",
                "Timestamp"
            ])


def rotate_log_daily():
    while True:
        now = datetime.datetime.now(PAKISTAN_TZ)
        next_midnight = (now + datetime.timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = (next_midnight - now).total_seconds()
        time.sleep(seconds_until_midnight + 1)
        ensure_log_file()


@app.route('/')
def index():
    filename = get_today_log_filename()
    if not os.path.exists(filename):
        return render_template("index.html", headers=[], data=[])

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if not rows:
            return render_template("index.html", headers=[], data=[])

        headers = rows[0]
        data = rows[1:]
    return render_template("index.html", headers=headers, data=data)


@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()
    required = [
        "device_id", "whatsapp_type", "number", "message_type", "timestamp"
    ]
    if not data or not all(field in data for field in required):
        return jsonify({"error": "Missing or invalid data"}), 400

    filename = get_today_log_filename()
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            data['device_id'], data['whatsapp_type'], data['number'],
            data['message_type'], data['timestamp']
        ])
    return jsonify({"status": "Logged successfully"}), 200


@app.route('/download')
def download():
    filename = get_today_log_filename()
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "No log found", 404


@app.route('/upload', methods=['POST'])
def upload():
    return jsonify({"status": "This will upload to Google Drive"}), 200


if __name__ == '__main__':
    ensure_log_file()
    Thread(target=rotate_log_daily, daemon=True).start()
    app.run(host='0.0.0.0', port=3001, debug=True)
