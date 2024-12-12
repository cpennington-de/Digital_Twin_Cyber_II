from urllib.parse import urlparse
import dns.resolver
import whois
import requests
from datetime import datetime

def extract_selected_features(url):
    features = {}
    parsed = urlparse(url)
    domain = parsed.netloc
    file_path = parsed.path

    # Helper function to count occurrences
    def count_char(text, char):
        return text.count(char)

    # URL and domain features
    features['length_url'] = len(url)
    features['domain_length'] = len(domain)

    # Directory features
    features['qty_plus_directory'] = count_char(file_path, '+')
    features['directory_length'] = len(file_path)
    features['qty_slash_directory'] = count_char(file_path, '/')
    features['qty_hyphen_directory'] = count_char(file_path, '-')
    features['qty_tilde_directory'] = count_char(file_path, '~')
    features['qty_at_directory'] = count_char(file_path, '@')
    features['qty_and_directory'] = count_char(file_path, '&')

    # File features
    features['file_length'] = len(file_path.split('/')[-1])
    features['qty_dot_file'] = count_char(file_path, '.')
    features['qty_hyphen_file'] = count_char(file_path, '-')
    features['qty_plus_file'] = count_char(file_path, '+')
    features['qty_equal_file'] = count_char(file_path, '=')

    # Email detection
    features['email_in_url'] = int('@' in url and '.com' in url)

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
        # WHOIS features
        domain_info = whois.whois(domain)
        features['time_domain_activation'] = domain_info.creation_date.timestamp() if domain_info.creation_date else 0
        features['time_domain_expiration'] = domain_info.expiration_date.timestamp() if domain_info.expiration_date else 0
    except:
        features['time_domain_activation'] = 0
        features['time_domain_expiration'] = 0

    try:
        # Response time and redirects
        response = requests.get(url, timeout=5)
        features['time_response'] = response.elapsed.total_seconds()
        features['qty_redirects'] = len(response.history)
    except:
        features['time_response'] = 0
        features['qty_redirects'] = 0

    return features

# Example usage
print(extract_selected_features("https://github.com/cpennington-de/Digital_Twin_Cyber_II/pull/4"))
