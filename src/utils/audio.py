import wave
import openai
import pyaudio
import keyboard
from os import getenv
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
INPUT_WAV_PATH = "src/artifacts/input.wav"

openai.api_key = OPENAI_API_KEY


# function to get the user's input audio
def record_and_transcribe_audio() -> str:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    print("Recording...")
    while keyboard.is_pressed("RIGHT_SHIFT"):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(INPUT_WAV_PATH, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    return transcribe_audio()


# function to transcribe the user's audio
def transcribe_audio() -> str:
    try:
        audio_file = open(INPUT_WAV_PATH, "rb")

        # Translating the audio to English
        # transcript = openai.Audio.translate("whisper-1", audio_file)

        # Transcribe the audio to detected language
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print("You: " + transcript.text)
        return transcript.text
    except Exception as error:
        print(f"error transcribing audio: {error}")
        return
