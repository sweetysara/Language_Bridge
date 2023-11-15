from googletrans import Translator
from gtts import gTTS
import os

def translate_to_malayalam(text, target_language='ml'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def text_to_speech(text, language='ml', output_file='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    os.system("start " + output_file)  # Open the audio file

if __name__ == '__main__':
    # Get English text input from the user
    english_text = input("Enter English text: ")

    # Translate to Malayalam
    malayalam_text = translate_to_malayalam(english_text)

    # Print the translated text
    print("Malayalam Translation:", malayalam_text)

    # Convert Malayalam text to speech
    text_to_speech(malayalam_text, language='ml', output_file='malayalam_output.mp3')
