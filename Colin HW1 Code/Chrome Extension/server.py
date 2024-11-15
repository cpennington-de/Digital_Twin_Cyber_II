from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# List of common phishing keywords
PHISHING_KEYWORDS = [
    "urgent", "important", "verify", "update", "suspicious",
    "account", "password", "security", "click here", "free",
    "reward", "won", "prize", "login", "confirm"
]

# Function to highlight and underline phishing text
def highlight_phishing(text):
    highlighted_text = text
    
    # Highlight and underline phishing keywords
    for keyword in PHISHING_KEYWORDS:
        highlighted_text = re.sub(
            rf'\b({keyword})\b',
            f"<span style='color: red; text-decoration: underline;'><strong>\\1</strong></span>",
            highlighted_text,
            flags=re.IGNORECASE
        )
    
    # Highlight and underline suspicious URLs
    highlighted_text = re.sub(
        r'(https?://[^\s]+)',
        f"<span style='color: yellow; text-decoration: underline;'><strong>\\1</strong></span>",
        highlighted_text
    )

    return highlighted_text

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    highlighted_text = data.get('text', '')

    # Highlight potential phishing attempts
    processed_text = highlight_phishing(highlighted_text)

    # Optionally, append ':)' to each line (if still needed)
    processed_lines = [line + '' for line in processed_text.splitlines()]
    
    # Join the processed lines back into a single string
    processed_text_with_smiley = '<br>'.join(processed_lines)

    return jsonify({"processed_text": processed_text_with_smiley})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs on http://127.0.0.1:5000
