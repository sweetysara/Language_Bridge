import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
def record_audio(duration, filename):
    # Record audio for the specified duration
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * 44100), samplerate=44100, channels=2)
    sd.wait()
    sf.write(filename, myrecording, 44100)

if __name__ == '__main__':
    filename = "recorded_audio.wav"
    duration = 5  # seconds

    record_audio(duration, filename)
    print(f"Recording stopped. Audio saved as {filename}")
    filename = "recorded_audio.wav"
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
        audio_data = r.record(source)
    # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)