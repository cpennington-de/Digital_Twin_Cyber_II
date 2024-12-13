from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS extension
import pandas as pd
from urllib.parse import urlparse, parse_qs
import re
import dns.resolver
import whois
import requests
import socket
import ssl
from datetime import datetime
import joblib

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def extract_features(url):
    features = {}
    parsed = urlparse(url)
    domain = parsed.netloc
    file_path = parsed.path

    # Helper function to count occurrences
    def count_char(text, char):
        return text.count(char)

    # Extract features in the specified order

    # URL and domain features
    features['length_url'] = len(url)
    features['domain_length'] = len(domain)

    # Directory features
    features['qty_hyphen_directory'] = count_char(file_path, '-')
    features['qty_slash_directory'] = count_char(file_path, '/')
    features['qty_at_directory'] = count_char(file_path, '@')
    features['qty_tilde_directory'] = count_char(file_path, '~')
    features['qty_plus_directory'] = count_char(file_path, '+')
    features['directory_length'] = len(file_path)

    # File features
    features['qty_dot_file'] = count_char(file_path, '.')
    features['qty_hyphen_file'] = count_char(file_path, '-')
    features['qty_equal_file'] = count_char(file_path, '=')
    features['qty_plus_file'] = count_char(file_path, '+')
    features['file_length'] = len(file_path.split('/')[-1])

    # Email detection
    features['email_in_url'] = int('@' in url and '.com' in url)

    try:
        # Response time
        response = requests.get(url, timeout=5)
        features['time_response'] = response.elapsed.total_seconds()
    except:
        features['time_response'] = 0

    try:
        # WHOIS features
        domain_info = whois.whois(domain)
        features['time_domain_activation'] = domain_info.creation_date.timestamp() if domain_info.creation_date else 0
        features['time_domain_expiration'] = domain_info.expiration_date.timestamp() if domain_info.expiration_date else 0
    except:
        features['time_domain_activation'] = 0
        features['time_domain_expiration'] = 0

    try:
        # DNS features
        resolver = dns.resolver.Resolver()
        dns_records = resolver.resolve(domain, 'A')
        features['qty_ip_resolved'] = len(dns_records)
        features['ttl_hostname'] = dns_records.rrset.ttl
    except:
        features['qty_ip_resolved'] = 0
        features['ttl_hostname'] = 0

    try:
        # Redirects
        response = requests.get(url, timeout=5)
        features['qty_redirects'] = len(response.history)
    except:
        features['qty_redirects'] = 0

    return features

model = joblib.load('Random_Forest_Classifiers.pkl')



@app.route('/extract-features', methods=['POST'])
def extract_url_features():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        features = extract_features(url)
        if features:  # Add this check
            df = pd.DataFrame([features])
            #print(url)
            df.to_csv('url_features.csv', index=False)
            return jsonify(features)  # Return features directly
        else:
            return jsonify({'error': 'Failed to extract features'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
        



def Phishing_Detection_Model(Extracted_DATA):
    try:
        # Ensure the DataFrame matches the input format of the model
        prediction = model.predict(Extracted_DATA)
        print(prediction)
        
        # Return True if the site is predicted as phishing (1), otherwise False
        return bool(prediction[0])
    except Exception as e:
        print(f"Error in model prediction: {str(e)}")
        return False  # Default to non-phishing in case of an error


# This function runs each time a piece of text is posted to the server
# It now returns True if "Google" is in the text and False otherwise
#model = joblib.load('/Users/colinpennington/Documents/GitHub/Digital_Twin_Cyber_II/Digital Twin HW2/Chrome Extension/decision_tree_with_knn_features.pkl')

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Extract features
        features = extract_features(url)
        if features:
            extracted_features = pd.DataFrame([features])
            extracted_features.to_csv('url_features.csv', index=False)
            
            # Phishing detection
            prediction = Phishing_Detection_Model(extracted_features)
            
            return jsonify({
                'features': features,
                'is_phishing': bool(prediction)  # Return as True/False
            })
        else:
            return jsonify({'error': 'Failed to extract features'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


def Phishing_Detection_Model(Extracted_DATA):
    
    try:
        # Ensure the DataFrame matches the input format of the model
        prediction = model.predict(Extracted_DATA)
        
        # Return True if the site is predicted as phishing (1), otherwise False
        return bool(prediction[0])
    except Exception as e:
        print(f"Error in model prediction: {str(e)}")
        return False  # Default to non-phishing in case of an error

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs on http://127.0.0.1:5000




