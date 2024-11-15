import nltk
nltk.download('punkt')
nltk.download('stopwords')
import email
from email import policy
from email.parser import BytesParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
import sys

# Function to read the content of the text file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()



def clean_polite_phrases(text):
    # List of common polite phrases and greetings to filter out
    polite_phrases = [
        "hello", "hi", "dear", "good morning", "good afternoon", 
        "thank you", "thanks", "regards", "best regards", "best wishes",
        "sincerely", "well wishes", "all the best", "take care", 
        "warm regards", "looking forward", "kind regards"
    ]
    
    # Remove sentences with polite phrases
    sentences = sent_tokenize(text)
    filtered_sentences = [
        sentence for sentence in sentences
        if not any(phrase in sentence.lower() for phrase in polite_phrases)
    ]
    
    return ' '.join(filtered_sentences)

   

def summarize_email(file_path):
    # Step 1: Open and parse the email file
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    # Extract the email body
    body = msg.get_body(preferencelist=('plain')).get_content()
    
    # Step 1.2: Clean out polite phrases
    body = clean_polite_phrases(body)

    # Step 2: Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(body)
    words = [word for word in words if word.lower() not in stop_words and word.isalnum()]
    
    # Step 3: Sentence tokenization
    sentences = sent_tokenize(body)
    
    # Step 4: Scoring sentences based on word frequency
    word_frequencies = {}
    for word in words:
        if word.lower() not in stop_words:
            word_frequencies[word.lower()] = word_frequencies.get(word.lower(), 0) + 1
    
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
    
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]
      # Step 5: Select the top sentences for summary                
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]
    summary = ' '.join(summary_sentences)
    
    return summary                 
    
file_path = '/Users/colinpennington/Gradschool/Cyber Security II/HW1 CODE/Python Summary/Email.txt'
summary = summarize_email(file_path)
print("Email Summary:\n", summary)


#method for using arguments instead of a hardcoded filepath
"""
# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_text_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        email_content = read_file(file_path)
        summary = summarize_email(email_content)
        print("Summary:\n", summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

"""
