import wave
import pyaudio
import winsound
import keyboard
from scipy.io import wavfile
from os import getenv
from dotenv import load_dotenv
from vits.index import vits
from faster_whisper import WhisperModel

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
INPUT_WAV_PATH = "src/artifacts/input.wav"
TTS_WAV_PATH = "src/artifacts/tts.wav"
WHISPER_MODEL_DIR = "src/whisper_model"  # model is "small.en"

whisper = WhisperModel(WHISPER_MODEL_DIR, device="cpu", compute_type="int8")


# function to get the user's input audio
def record_audio() -> str:
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
    print("Stopped recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(INPUT_WAV_PATH, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
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


def generate_audio(text):
    status, audios, time = vits(text)
    wavfile.write(TTS_WAV_PATH, audios[0], audios[1])
