from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["webseeder_chatbot"]
messages_collection = db["messages"]

def save_message(sender, message):
    messages_collection.insert_one({
        "sender": sender,
        "message": message
    })
