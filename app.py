from flask import Flask, render_template, request, jsonify
import logging
from chatbot.logic import handle_message
from services.karnataka_board_service import get_board_overview

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json() or {}
    message = payload.get("message", "")
    # session_data could be passed here if you implement sessions
    reply, meta = handle_message(message, session_data=None)
    return jsonify({"reply": reply, "meta": meta})

@app.route("/api/board/<board_key>", methods=["GET"])
def api_board_info(board_key):
    data = get_board_overview(board_key)
    if not data:
        return jsonify({"error": "Board not found"}), 404
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

# app.py or settings.py

import os
from dotenv import load_dotenv

# This function finds the .env file and loads the key-value pairs
# into the environment variables (os.environ).
load_dotenv() 

# Now you can access the variables using os.getenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ('true', '1', 't')


# Example usage:
if DEBUG_MODE:
    print("Application running in debug mode.")

# The actual secrets are read from the local .env file,
# which is safely ignored by Git!