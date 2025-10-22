import json
import random
import os
import nltk
from nltk.stem import WordNetLemmatizer
import logging
import difflib

logger= logging.getLogger(__name__)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logger.info("Downloading punkt tokenizer...")
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    logger.info("Downloading wordnet...")
    nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

try:
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        intents = json.load(f)

    if not isinstance(intents, dict) or "intents" not in intents:
        raise ValueError("intents.json must contain an 'intents' key with a list")
    if not isinstance(intents["intents"], list):
        raise ValueError("'intents' must be a list")

except FileNotFoundError:
    logger.error(f"intents.json not found at {INTENTS_PATH}")
    raise
except (json.JSONDecodeError, ValueError) as e:
    logger.error(f"Invalid intents.json format: {e}")
    raise



def tokenize_and_lemmatize(sentence):
    """Tokenize and lemmatize a sentence."""
    tokens = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(w.lower()) for w in tokens]


def find_intent(user_message: str):
    """Find the best matching intent using sequence similarity."""
    best_intent = None
    best_score = 0.0
    threshold = 0.6  # Adjust sensitivity

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            score = difflib.SequenceMatcher(
                None,
                user_message.lower(),
                pattern.lower()
            ).ratio()

            if score > best_score and score >= threshold:
                best_score = score
                best_intent = intent

    return best_intent


def handle_chat_message(user_message: str) -> str:
    """Return response strictly from intents.json"""
    intent = find_intent(user_message)

    if intent:
        return random.choice(intent["responses"])
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"
