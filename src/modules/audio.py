import wave
import pyaudio
import winsound
import keyboard
from os import getenv
from dotenv import load_dotenv

load_dotenv()

INPUT_WAV_PATH = getenv("INPUT_WAV_PATH")
TTS_WAV_PATH = getenv("TTS_WAV_PATH")
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100


def init_recorder():
    return pyaudio.PyAudio()


# function to get the user's input audio
def record_audio(recorder) -> str:
    stream = recorder.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    print("Recording...")
    while keyboard.is_pressed("RIGHT_SHIFT"):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped recording")
    stream.stop_stream()
    stream.close()
    wf = wave.open(INPUT_WAV_PATH, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(recorder.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


def play_audio():
    winsound.PlaySound(TTS_WAV_PATH, winsound.SND_FILENAME)
