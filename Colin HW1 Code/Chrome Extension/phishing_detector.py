#Code used to build out server.py. Not used for any function at the moment.


import re
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# List of common phishing keywords
PHISHING_KEYWORDS = [
    "urgent", "important", "verify", "update", "suspicious",
    "account", "password", "security", "click here", "free",
    "reward", "won", "prize", "login", "confirm"
]

# Function to highlight phishing text
def highlight_phishing(text):
    highlighted_text = text
    
    # Highlight phishing keywords
    for keyword in PHISHING_KEYWORDS:
        highlighted_text = re.sub(rf'\b({keyword})\b', f"{Fore.RED}{Style.BRIGHT}\\1{Style.RESET_ALL}", highlighted_text, flags=re.IGNORECASE)
    
    # Highlight suspicious URLs
    highlighted_text = re.sub(r'(https?://[^\s]+)', f"{Fore.YELLOW}{Style.BRIGHT}\\1{Style.RESET_ALL}", highlighted_text)

    return highlighted_text

if __name__ == "__main__":
    # Input text
    text = input("Enter the text to analyze for phishing attempts:\n")
    
    # Highlight phishing attempts
    result = highlight_phishing(text)
    
    # Display the highlighted text
    print("\nHighlighted Text:")
    print(result)
