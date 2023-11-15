import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from googletrans import Translator

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

if __name__ == '__main__':
    filename = "recorded_audio.wav"
    duration = 5  # seconds

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

