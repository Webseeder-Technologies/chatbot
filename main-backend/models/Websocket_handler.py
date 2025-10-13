import json
import random
import os
import nltk
from nltk.stem import WordNetLemmatizer
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

    patterns = []
    pattern_intent_map = []

    for intent in intents["intents"]:
        for pattern in intent.get("patterns", []):
            patterns.append(pattern)
            pattern_intent_map.append(intent)

    if not patterns:
        return None

    try:
        vectorized = TfidfVectorizer().fit_transform([user_message] + patterns)
    except ValueError:
        return None

    similarities = cosine_similarity(vectorized[0:1], vectorized[1:]).flatten()
    best_idx = similarities.argmax()
    best_score = similarities[best_idx]

    if best_score >= 0.3:
        return pattern_intent_map[best_idx]
    return None

def handle_chat_message(user_message: str) -> str:
    """Return response strictly from intents.json"""
    intent = find_intent(user_message)

    if intent:
        return random.choice(intent["responses"])
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"
