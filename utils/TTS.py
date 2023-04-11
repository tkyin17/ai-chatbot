import requests
import urllib.parse
from utils.katakana import *


def voicevox_tts(tts):
    # You need to run VoicevoxEngine.exe first before running this script

    # voicevox via docker
    voicevox_url = "http://localhost:50021"

    # voicevox via colab
    # voicevox_url = "https://warm-parts-float-34-69-1-252.loca.lt"

    # Convert the text to katakana. Example: ORANGE -> オレンジ, so the voice will sound more natural
    katakana_text = katakana_converter(tts)

    # You can change the voice to your liking. You can find the list of voices on speaker.json
    # or check the website https://voicevox.hiroshiba.jp
    params_encoded = urllib.parse.urlencode({"text": katakana_text, "speaker": 46})
    request = requests.post(f"{voicevox_url}/audio_query?{params_encoded}")
    params_encoded = urllib.parse.urlencode(
        {"speaker": 46, "enable_interrogative_upspeak": True}
    )
    request = requests.post(
        f"{voicevox_url}/synthesis?{params_encoded}", json=request.json()
    )

    with open("output.wav", "wb") as outfile:
        outfile.write(request.content)
