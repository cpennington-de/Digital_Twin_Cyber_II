import re
import sys

def extract_email_data(email_text):
    # Define patterns for extraction
    sender_pattern = r"From:\s*(.*?)(?=\n|$)"
    receiver_pattern = r"To:\s*(.*?)(?=\n|$)"
    link_pattern = r"https?://[^\s]+"
    keywords = ['urgent', 'important', 'action required']  # Add more keywords as needed
    
    # Extract sender
    sender_match = re.search(sender_pattern, email_text, re.IGNORECASE)
    sender = sender_match.group(1).strip() if sender_match else None
    
    # Extract receiver
    receiver_match = re.search(receiver_pattern, email_text, re.IGNORECASE)
    receiver = receiver_match.group(1).strip() if receiver_match else None
    
    # Extract links
    links = re.findall(link_pattern, email_text)
    
    # Extract keywords
    found_keywords = [word for word in keywords if word in email_text.lower()]

    return {
        "sender": sender,
        "receiver": receiver,
        "links": links,
        "keywords": found_keywords
    }

def read_file(file_path):
    """Reads the content of a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main(file_path):
    # Read the email text from the provided file
    email_text = read_file(file_path)

    # Extract data from the email
    extracted_data = extract_email_data(email_text)

    # Print the extracted data
    print("Extracted Data:")
    print(f"Sender: {extracted_data['sender']}")
    print(f"Receiver: {extracted_data['receiver']}")
    print(f"Links: {extracted_data['links']}")
    print(f"Keywords: {extracted_data['keywords']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_email.py <path_to_text_file>")
    else:
        file_path = sys.argv[1]
        main(file_path)
