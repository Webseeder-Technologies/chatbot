import random
import json
import pickle
import numpy as np
import os
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
nltk_data_path = os.path.join(BASE_DIR, ".venv", "nltk_data")



# Add nltk_data_path to nltk's search paths if not already present
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)

def unzip_wordnet_if_needed():
    """
    When nltk downloads wordnet in a virtualenv, it sometimes
    saves it as a zip file instead of extracted folder.
    This function extracts wordnet.zip if it exists.
    """
    corpora_dir = os.path.join(nltk_data_path, "corpora")
    wordnet_dir = os.path.join(corpora_dir, "wordnet")
    wordnet_zip = os.path.join(corpora_dir, "wordnet.zip")

    if not os.path.isdir(wordnet_dir) and os.path.isfile(wordnet_zip):
        print(f"Extracting {wordnet_zip} to {corpora_dir} ...")
        with zipfile.ZipFile(wordnet_zip, 'r') as zip_ref:
            zip_ref.extractall(corpora_dir)
        print("Extraction done.")
    else:
        print("Wordnet already extracted or zip missing.")


# print("NLTK data after adding:", nltk.data.path)

def check_nltk_resources():
    """
    Checks if required nltk resources are available.
    If not found, tries to unzip wordnet.zip,
    then attempts to download missing resources automatically.
    Raises RuntimeError if resources still missing after this.
    """
     
    required_resources = ["tokenizers/punkt", "corpora/wordnet"]
    missing = []
    for resource in required_resources:
        try:
            nltk.data.find(resource)
        except LookupError:
            missing.append(resource)

    if missing:
        raise RuntimeError(
            f"Missing NLTK resources: {', '.join(missing)}. "
            "Please install them at build or deploy time using nltk.download(). "
            "For example, run: python -m nltk.downloader punkt wordnet"
        )
    
unzip_wordnet_if_needed()
check_nltk_resources() 

lemmatizer = WordNetLemmatizer()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
            "⚡ I’m still learning! Can you try asking differently?",
            "🙋 You can ask me about our services like web development, app development, AI solutions, and more!"
        ])

    tag = intents_list[0]["intent"]
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, something went wrong finding a response."
