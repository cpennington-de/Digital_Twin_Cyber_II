from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# This function runs each time a piece of text is posted to the server
# It now returns True if "Google" is in the text and False otherwise
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text', '')
    contains_google = "bing" in text  # Check if "Google" is in the text
    return jsonify({"contains_google": contains_google})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs on http://127.0.0.1:5000
