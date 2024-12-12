from urllib.parse import urlparse
import dns.resolver
import whois
import requests
import ssl
import socket
from datetime import datetime

def extract_features(url):
    features = {}
    parsed = urlparse(url)
    domain = parsed.netloc 
    
    # Helper function to count occurrences
    def count_char(text, char):
        return text.count(char)

    # Character counts
    features['qty_slash_url'] = count_char(url, '/')
    features['qty_dot_url'] = count_char(url, '.')
    features['qty_hyphen_url'] = count_char(url, '-')
    features['qty_at_url'] = count_char(url, '@')
    features['qty_questionmark_url'] = count_char(url, '?')
    features['qty_equal_url'] = count_char(url, '=')
    features['qty_underline_url'] = count_char(url, '_')
    features['qty_and_url'] = count_char(url, '&')
    features['qty_tilde_url'] = count_char(url, '~')
    features['qty_comma_url'] = count_char(url, ',')
    features['qty_percent_url'] = count_char(url, '%')
    features['qty_asterisk_url'] = count_char(url, '*')
    features['qty_hashtag_url'] = count_char(url, '#')
    features['qty_dollar_url'] = count_char(url, '$')
    features['qty_space_url'] = count_char(url, ' ')

    # Domain length
    features['domain_length'] = len(domain)

    # Top-Level Domain Check
    tld = domain.split('.')[-1]
    common_tlds = ['com', 'org', 'net', 'edu', 'gov']
    features['qty_tld_url'] = int(tld in common_tlds)

    # Email detection
    features['email_in_url'] = int('@' in url and '.com' in url)

    # Vowel count in domain
    features['qty_vowels_domain'] = sum(1 for char in domain if char.lower() in 'aeiou')

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

print(extract_features("https://github.com/cpennington-de/Digital_Twin_Cyber_II/pull/4"))


from urllib.parse import urlparse

def extract_file_path_features(url):
    features = {}
    parsed = urlparse(url)
    file_path = parsed.path  # Extract the file path part of the URL

    # Helper function to count occurrences
    def count_char(text, char):
        return text.count(char)
    
    # File-path-related features
    features['qty_slash_directory'] = count_char(file_path, '/')
    features['qty_questionmark_file'] = count_char(file_path, '?')
    features['qty_dollar_file'] = count_char(file_path, '$')
    features['qty_hashtag_file'] = count_char(file_path, '#')
    features['qty_slash_file'] = count_char(file_path, '/')
    features['qty_hashtag_directory'] = count_char(file_path, '#')
    features['qty_questionmark_directory'] = count_char(file_path, '?')
    features['qty_at_file'] = count_char(file_path, '@')
    features['qty_exclamation_file'] = count_char(file_path, '!')
    features['qty_and_file'] = count_char(file_path, '&')
    features['qty_tilde_file'] = count_char(file_path, '~')
    features['qty_equal_file'] = count_char(file_path, '=')
    features['qty_space_file'] = count_char(file_path, ' ')
    features['qty_comma_file'] = count_char(file_path, ',')
    features['qty_comma_directory'] = count_char(file_path, ',')
    features['qty_exclamation_directory'] = count_char(file_path, '!')
    features['qty_space_directory'] = count_char(file_path, ' ')
    features['qty_tilde_directory'] = count_char(file_path, '~')
    features['qty_equal_directory'] = count_char(file_path, '=')
    features['qty_plus_file'] = count_char(file_path, '+')
    features['qty_dollar_directory'] = count_char(file_path, '$')
    features['qty_dot_file'] = count_char(file_path, '.')
    features['qty_plus_directory'] = count_char(file_path, '+')
    features['qty_and_directory'] = count_char(file_path, '&')
    features['directory_length'] = len(file_path)
    features['file_length'] = len(file_path.split('/')[-1])  # Length of the file name
    features['qty_asterisk_file'] = count_char(file_path, '*')
    features['qty_asterisk_directory'] = count_char(file_path, '*')
    features['qty_underline_file'] = count_char(file_path, '_')
    features['qty_underline_directory'] = count_char(file_path, '_')
    features['qty_hyphen_file'] = count_char(file_path, '-')
    features['qty_hyphen_directory'] = count_char(file_path, '-')
    features['qty_percent_file'] = count_char(file_path, '%')
    features['qty_percent_directory'] = count_char(file_path, '%')
    
    return features


print(extract_file_path_features("https://github.com/cpennington-de/Digital_Twin_Cyber_II/pull/4"))