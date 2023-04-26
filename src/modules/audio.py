import wave

import winsound
import keyboard
from os import getenv
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
INPUT_WAV_PATH = getenv("INPUT_WAV_PATH")
TTS_WAV_PATH = getenv("TTS_WAV_PATH")
WHISPER_MODEL_DIR = getenv("WHISPER_MODEL_DIR")  # model is "small.en"
DEVICE = getenv("DEVICE")
FORMAT = None
CHUNK = 1024
CHANNELS = 1
RATE = 44100

whisper = WhisperModel(WHISPER_MODEL_DIR, device=DEVICE, compute_type="int8")


def init_recorder():
    import pyaudio

    global FORMAT
    FORMAT = pyaudio.paInt16

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


# function to transcribe the user's audio
def transcribe_audio() -> str:
    try:
        segment_generator, _ = whisper.transcribe(INPUT_WAV_PATH, beam_size=5)
        transcript = ""
        for segment in segment_generator:
            transcript = transcript + segment.text
        transcript = transcript.strip()
        print("You: " + transcript)
        return transcript
    except Exception as error:
        print(f"error transcribing audio: {error}")
        return


def play_audio():
    winsound.PlaySound(TTS_WAV_PATH, winsound.SND_FILENAME)
