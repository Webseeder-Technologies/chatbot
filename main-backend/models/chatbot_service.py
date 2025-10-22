import random
import json
import pickle
import numpy as np
import os
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

lemmatizer = WordNetLemmatizer()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Download NLTK resources (once)
nltk.download("punkt")
nltk.download("wordnet")


# Paths
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")


# Load model and data
with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents = json.load(file)
words = pickle.load(open(os.path.join(BASE_DIR, "words.pkl"), "rb"))
classes = pickle.load(open(os.path.join(BASE_DIR, "classes.pkl"), "rb"))
model = load_model(os.path.join(BASE_DIR, "chatbot_webseedermodel.keras"))

# Preprocess sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Convert to bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

# Predict intent
def predict_class(sentence, threshold=0.2):
    if "about webseeder" in sentence.lower():
        return [{"intent": "about", "probability": "1.0"}]
    if sentence.lower().strip() in ["service", "services"]:
        return [{"intent": "services", "probability": "1.0"}]

    bow = bag_of_words(sentence)
    if np.sum(bow) == 0:
        return []

    res = model.predict(np.array([bow]), verbose=0)[0]
    results = [{"intent": classes[i], "probability": str(prob)}
               for i, prob in enumerate(res) if prob > threshold]

    results.sort(key=lambda x: float(x["probability"]), reverse=True)
    return results

# Get response
def get_response(user_input):
    intents_list = predict_class(user_input)
    if not intents_list:
        return random.choice([
            "🤔 Sorry, I didn’t understand that. Could you rephrase?",
            "⚡ I'm still learning! Can you try asking differently?",
            "🙋 You can ask me about our services like web development, app development, AI solutions, and more!"
        ])

    tag = intents_list[0]["intent"]
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, something went wrong finding a response."
