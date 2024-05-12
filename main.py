import json

from flask import Flask, render_template, request, jsonify
import os
from dotenv import dotenv_values
from openai import OpenAI
from functions import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/ask", methods=['POST'])
def ask_assistant():
    config = dotenv_values(".env")
    API_KEY = config['API_KEY']
    ASSISTANT_ID = config['ASSISTANT_ID']
    client = OpenAI(api_key=API_KEY)
    # Create Thread
    thread_id = create_thread(client)
    data = request.get_json()
    query = data['query']
    # Create Message
    message_id = create_message(client, thread_id, query)

    # Create Runa and Get Response
    message = create_run_messages(client, thread_id, ASSISTANT_ID)
    message = json.loads(message)
    return jsonify({'data': message}), 200


if __name__ == "__main__":
    app.run(debug=True)
