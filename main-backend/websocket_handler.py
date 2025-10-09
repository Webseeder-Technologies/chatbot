import json
import random
import os
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "intents.json"))

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)


def tokenize_and_lemmatize(sentence):
    """Tokenize and lemmatize a sentence."""
    tokens = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(w.lower()) for w in tokens]


def find_intent(user_message: str):
    """Find the best matching intent for a user message."""
    tokens = tokenize_and_lemmatize(user_message)

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = tokenize_and_lemmatize(pattern)
            if all(word in tokens for word in pattern_tokens):
                return intent

    return None


def handle_chat_message(user_message: str) -> str:
    """Return response strictly from intents.json"""
    intent = find_intent(user_message)

    if intent:
        return random.choice(intent["responses"])
    else:
        return "Sorry, I didn’t understand that. Can you rephrase?"
