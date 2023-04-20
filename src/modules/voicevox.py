import requests
import urllib.parse
from os import getenv
from dotenv import load_dotenv
from modules.katakana import *

load_dotenv()

USE_VOICEVOX_COLAB = getenv("USE_VOICEVOX_COLAB", "False").lower() in ("true", "1", "t")
VOICE_ID = getenv("VOICE_ID")
TTS_WAV_PATH = "src/artifacts/tts.wav"

if USE_VOICEVOX_COLAB:
    VOICEBOX_URL = "https://warm-parts-float-34-69-1-252.loca.lt"
else:
    VOICEBOX_URL = "http://localhost:50021"


def get_voicevox_tts(text: str) -> None:
    # Convert the text to katakana. Example: ORANGE -> オレンジ, so the voice will sound more natural
    katakana_text = katakana_converter(text)

    # You can change the voice to your liking. You can find the list of voices on speaker.json
    # or check the website https://voicevox.hiroshiba.jp
    params_encoded = urllib.parse.urlencode(
        {"text": katakana_text, "speaker": VOICE_ID}
    )
    request = requests.post(f"{VOICEBOX_URL}/audio_query?{params_encoded}")

    if request.status_code == 404:
        print("Unable to reach Voicevox engine, please check that it is running.")
        return

    params_encoded = urllib.parse.urlencode(
        {"enable_interrogative_upspeak": True, "speaker": VOICE_ID}
    )
    request = requests.post(
        f"{VOICEBOX_URL}/synthesis?{params_encoded}", json=request.json()
    )

    with open(TTS_WAV_PATH, "wb") as outfile:
        outfile.write(request.content)
