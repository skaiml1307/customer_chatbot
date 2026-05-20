import nltk
import re
from nltk.tokenize import word_tokenize
from rapidfuzz import fuzz

# Download NLTK resources (only once)
nltk.download('punkt')
nltk.download('punkt_tab')

# Define keyword groups
keywords = {
    "greeting": ["hello", "hi", "hey", "greetings"],
    "hours": ["hours", "time", "open", "closing", "schedule", "timing"],
    "location": ["location", "located", "address", "office", "place", "branch"],
    "pricing": ["price", "cost", "charges", "fees", "rate", "pricing"],
    "politeness": ["thank", "thanks", "thankyou"],
    "farewell": ["bye", "goodbye", "see", "later", "farewell", "byee", "byeee", "exit", "quit"]
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)          # remove punctuation
    text = re.sub(r'(.)\1+', r'\1', text)        # reduce repeated letters
    return text

def match_token(token, category_words, threshold=70):  # lowered threshold for 2-letter misspellings
    for word in category_words:
        if fuzz.ratio(token, word) >= threshold:
            return True
    return False

def chatbot_response(user_input):
    normalized = normalize_text(user_input)
    tokens = word_tokenize(normalized)

    if any(match_token(t, keywords["greeting"]) for t in tokens):
        return "Hello! How can I help you today?"
    elif any(match_token(t, keywords["hours"]) for t in tokens):
        return "Our customer service is available from 9 AM to 6 PM, Monday to Friday."
    elif any(match_token(t, keywords["location"]) for t in tokens):
        return "We are located at 123 Main Street, New Delhi."
    elif any(match_token(t, keywords["pricing"]) for t in tokens):
        return "Our pricing depends on the product. Could you specify which one?"
    elif any(match_token(t, keywords["politeness"]) for t in tokens):
        return "You're welcome! Happy to help."
    elif any(match_token(t, keywords["farewell"]) for t in tokens):
        return "Goodbye! Have a great day."
    else:
        return "I'm sorry, I don't understand that. Could you rephrase?"

# Only run interactive loop if executed directly
if __name__ == "__main__":
    print("Welcome to Customer Service Chatbot! Type 'exit' or say 'bye' to quit.\n")
    while True:
        user_input = input("You: ")
        normalized = normalize_text(user_input)
        if any(match_token(t, keywords["farewell"]) for t in word_tokenize(normalized)):
            print("Chatbot: Goodbye! Have a great day.")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)
