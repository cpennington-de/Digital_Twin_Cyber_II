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
    
    # Helper function to count occurrences
    def count_char(text, char):
        return text.count(char)
    
    # [Previous feature extraction code remains the same until Google/ASN features]
    
    try:
        # DNS features
        dns_start = datetime.now()
        resolver = dns.resolver.Resolver()
        dns_records = resolver.resolve(domain, 'A')
        features['qty_ip_resolved'] = len(dns_records)
        features['ttl_hostname'] = dns_records.rrset.ttl
        
        ns_records = resolver.resolve(domain, 'NS')
        features['qty_nameservers'] = len(ns_records)
        
        mx_records = resolver.resolve(domain, 'MX')
        features['qty_mx_servers'] = len(mx_records)
    except:
        features['qty_ip_resolved'] = 0
        features['ttl_hostname'] = 0
        features['qty_nameservers'] = 0
        features['qty_mx_servers'] = 0
    
    try:
        # WHOIS features
        domain_info = whois.whois(domain)
        features['time_domain_activation'] = domain_info.creation_date.timestamp() if domain_info.creation_date else 0
        features['time_domain_expiration'] = domain_info.expiration_date.timestamp() if domain_info.expiration_date else 0
    except:
        features['time_domain_activation'] = 0
        features['time_domain_expiration'] = 0
    
    try:
        # Response time
        response = requests.get(url, timeout=5)
        features['time_response'] = response.elapsed.total_seconds()
        features['qty_redirects'] = len(response.history)
    except:
        features['time_response'] = 0
        features['qty_redirects'] = 0
    
    try:
        # SSL/TLS certificate
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                features['tls_ssl_certificate'] = 1
    except:
        features['tls_ssl_certificate'] = 0
    
    # Server/client features
    try:
        ip = socket.gethostbyname(domain)
        features['server_client_domain'] = int(ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.'))
    except:
        features['server_client_domain'] = 0
    
    # SPF record
    try:
        spf_records = resolver.resolve(domain, 'TXT')
        features['domain_spf'] = any('spf' in str(record).lower() for record in spf_records)
    except:
        features['domain_spf'] = 0
    
    # URL shortening detection
    shortening_services = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl']
    features['url_shortened'] = any(service in domain.lower() for service in shortening_services)
    
    return features

model = joblib.load('decision_tree_with_knn_features.pkl')



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
        
        # Return True if the site is predicted as phishing (1), otherwise False
        return bool(prediction[0])
    except Exception as e:
        print(f"Error in model prediction: {str(e)}")
        return False  # Default to non-phishing in case of an error


# This function runs each time a piece of text is posted to the server
# It now returns True if "Google" is in the text and False otherwise
model = joblib.load('/Users/colinpennington/Documents/GitHub/Digital_Twin_Cyber_II/Digital Twin HW2/Chrome Extension/decision_tree_with_knn_features.pkl')

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        features = extract_features(url)  # Assume this function extracts features correctly
        if features:
            extracted_features = pd.DataFrame([features])
            extracted_features.to_csv('url_features.csv', index=False)
            
            # Pass the extracted features to the phishing detection model
            prediction = Phishing_Detection_Model(extracted_features)
            
            # Return the prediction along with the features
            return jsonify({
                'features': features,
                'is_phishing': prediction
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




