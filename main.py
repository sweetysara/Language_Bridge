import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from googletrans import Translator
from googletrans import Translator
from gtts import gTTS
import os
from pymongo import MongoClient

# Replace these with your MongoDB connection details
mongo_host = "localhost"
mongo_port = 27017
database_name = "queryres"
collection_name_user = "userid"
collection_name_orders = "orders"

client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
collection_user = db[collection_name_user]
collection_orders = db[collection_name_orders]
user_id = 60

def record_audio(duration, filename):
    # Record audio for the specified duration
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
    sd.wait()
    sf.write(filename, myrecording, 44100)

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def process_user_input(user_input):

    keywords = {
        "booking": ["book", "buy", "reserve"],
        "cancelling": ["cancel", "delete", "remove"]
        # Add more keywords as needed
    }

    for keyword, synonyms in keywords.items():
        if any(synonym in user_input.lower() for synonym in synonyms):
            return keyword

    return "enquiry"

def book_order(order_details):
    # Check if the user ID already exists in the collection
    existing_order = collection_orders.find_one({"user_id": order_details["user_id"]})

    if existing_order:
        # User ID already exists, return a response indicating that the order is already booked
        return "Order already booked for this user ID."
    else:
        # User ID doesn't exist, insert the order details
        db.orders.insert_one(order_details)
        return "Booking successful! Your order has been placed."


def cancel_order(user_id):
    # Check if the order with the given user_id exists in the "orders" collection
    existing_order = collection_orders.find_one({"user_id": user_id})

    if existing_order:
        # If the order exists, delete it
        collection_orders.delete_one({"user_id": user_id})
        return "Order cancellation successful."
    else:
        # If the order doesn't exist, return a response indicating so
        return "No order in this user ID."
def get_response(keyword):
    response = db.responses.find_one({"keyword": keyword})
    return (
        response["response"]
        if response
        else "Sorry, I couldn't find a suitable response."
    )
def translate_to_malayalam(text, target_language='ml'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_speech(text, language='ml', output_file='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from googletrans import Translator
from googletrans import Translator
from gtts import gTTS
import os
from pymongo import MongoClient

# Replace these with your MongoDB connection details
mongo_host = "localhost"
mongo_port = 27017
database_name = "queryres"
collection_name_user = "userid"
collection_name_orders = "orders"

client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
collection_user = db[collection_name_user]
collection_orders = db[collection_name_orders]
user_id = 60

def record_audio(duration, filename):
    # Record audio for the specified duration
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
    sd.wait()
    sf.write(filename, myrecording, 44100)

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def process_user_input(user_input):

    keywords = {
        "booking": ["book", "buy", "reserve"],
        "cancelling": ["cancel", "delete", "remove"]
        # Add more keywords as needed
    }

    for keyword, synonyms in keywords.items():
        if any(synonym in user_input.lower() for synonym in synonyms):
            return keyword

    return "enquiry"

def book_order(order_details):
    # Check if the user ID already exists in the collection
    existing_order = collection_orders.find_one({"user_id": order_details["user_id"]})

    if existing_order:
        # User ID already exists, return a response indicating that the order is already booked
        return "Order already booked for this user ID."
    else:
        # User ID doesn't exist, insert the order details
        db.orders.insert_one(order_details)
        return "Booking successful! Your order has been placed."


def cancel_order(user_id):
    # Check if the order with the given user_id exists in the "orders" collection
    existing_order = collection_orders.find_one({"user_id": user_id})

    if existing_order:
        # If the order exists, delete it
        collection_orders.delete_one({"user_id": user_id})
        return "Order cancellation successful."
    else:
        # If the order doesn't exist, return a response indicating so
        return "No order in this user ID."
def get_response(keyword):
    response = db.responses.find_one({"keyword": keyword})
    return (
        response["response"]
        if response
        else "Sorry, I couldn't find a suitable response."
    )
def translate_to_malayalam(text, target_language='ml'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_speech(text, language='ml', output_file='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    os.system("start " + output_file)

if __name__ == '__main__':
    filename = "recorded_audio.wav"
    duration = 5  # seconds
    user_id = 60
    record_audio(duration, filename)
    print(f"Recording stopped. Audio saved as {filename}")

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            # Specify the language model for Malayalam ('ml-IN')
            malayalam_text = r.recognize_google(audio_data, language='ml-IN')
            print("Malayalam Text:", malayalam_text)

            # Translate Malayalam text to English
            english_text = translate_text(malayalam_text)
            print("English Translation:", english_text)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        response_keyword = process_user_input(english_text)

        if response_keyword == "booking":
            order_details = {"user_id": user_id, "status": "booked"}
            response = book_order(order_details)
        elif response_keyword == "cancelling":
            user_id = user_id  # Replace with user identification logic
            response = cancel_order(user_id)
        else:
            response = get_response(response_keyword)

        print(response)  # Correct indentation

        malayalam_text = translate_to_malayalam(response)
        print("Malayalam Translation:", malayalam_text)
        text_to_speech(malayalam_text, language='ml', output_file='malayalam_output.mp3')
