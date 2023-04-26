from os import getenv
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()

INPUT_WAV_PATH = getenv("INPUT_WAV_PATH")
WHISPER_MODEL_DIR = getenv("WHISPER_MODEL_DIR")  # model is "small.en"
DEVICE = getenv("DEVICE")

whisper = WhisperModel(WHISPER_MODEL_DIR, device=DEVICE, compute_type="int8")


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
