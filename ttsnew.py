from googletrans import Translator
import pyttsx3

def translate_to_malayalam(text, target_language='ml'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_speech(text, language='ml'):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    # Get English text input from the user
    english_text = input("Enter English text: ")

    # Translate to Malayalam
    malayalam_text = translate_to_malayalam(english_text)

    # Print the translated text
    print("Malayalam Translation:", malayalam_text)

    # Convert Malayalam text to speech and read it out loud
    text_to_speech(malayalam_text, language='ml')
