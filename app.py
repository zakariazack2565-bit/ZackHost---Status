from flask import Flask, render_template, jsonify
import requests
import threading
import time
from datetime import datetime

# Create Flask app ? Flask application instances;./'
app = Flask(__name__)

# Website GonnA Monitored :
URL = "https://zackhost.lovable.app"

# Store monitoring history of the ping , latency , uptime e.g
history = []

# -----------------------------------
# CHECK WEBSITE FUNCTION
# -----------------------------------
def check_website():

    try:
        # Start timer
        start = time.time()

        # Send request to website
        response = requests.get(URL, timeout=5)

        # End timer
        end = time.time()

        # Calculate latency
        latency = round((end - start) * 1000, 2)

        # Get status code
        status_code = response.status_code

        # Website state
        state = "UP"

        if status_code != 200:
            state = "ISSUE"

        # Return result
        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": status_code,
            "latency": latency,
            "state": state
        }

    except:
        # Website failed
        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": 0,
            "latency": 0,
            "state": "DOWN"
        }

# -----------------------------------
# BACKGROUND MONITOR LOOP
# -----------------------------------
def monitor():

    while True:

        result = check_website()

        history.append(result)

        # Keep only last 50 checks
        if len(history) > 50:
            history.pop(0)

        # Wait 5 seconds for next monitor
        time.sleep(5)

# -----------------------------------
# HOME PAGE
# -----------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------------
# API FOR LIVE DATA
# -----------------------------------
@app.route("/api/status")
def status():
    return jsonify(history)

# -----------------------------------
# START SERVER
# -----------------------------------
if __name__ == "__main__":

    # Start monitoring thread
    thread = threading.Thread(target=monitor)

    thread.daemon = True
    thread.start()

    # Run website At host + port
    app.run(host="0.0.0.0", port=5000)