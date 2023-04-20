import sys
import json
import winsound
import requests
import googletrans
from utils.voicevox import get_voicevox_tts
from utils.subtitle import generate_subtitle

DEEPLX_URL = "http://localhost:1188/translate"
TTS_WAV_PATH = "src/artifacts/tts.wav"

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)


# translating is optional
def translate_text(text) -> str:
    # tts will be the string to be converted to audio
    detected_language = detect_language_google(text)
    # tts = translate_google(text, f"{detect}", "JA")
    tts = translate_deeplx(text, f"{detected_language}", "JA")
    tts_en = text
    try:
        # print("ID Answer: " + subtitle)
        print("JP Answer: " + tts)
        print("EN Answer: " + tts_en)
    except Exception as error:
        print(f"error translating text: {error}")
        return
    # Japanese TTS
    # get_voicevox_tts(tts)

    # Generate subtitle
    generate_subtitle(tts_en)

    return tts

    # winsound.PlaySound(TTS_WAV_PATH, winsound.SND_FILENAME)


def translate_deeplx(
    text: str, source_language_id: str, target_language_id: str
) -> str:
    # define the parameters for the translation request
    params = {
        "text": text,
        "source_lang": source_language_id,
        "target_lang": target_language_id,
    }

    # convert the parameters to a JSON string
    payload = json.dumps(params)

    # send the POST request with the JSON payload
    response = requests.post(
        url=DEEPLX_URL, headers={"Content-Type": "application/json"}, data=payload
    )

    # get the response data as a JSON object
    data = response.json()

    # extract the translated text from the response
    translated_text = data["data"]

    return translated_text


def translate_google(
    text: str, source_language_id: str, target_language_id: str
) -> str | None:
    try:
        translator = googletrans.Translator()
        result = translator.translate(
            text, src=source_language_id, dest=target_language_id
        )
        return result.text
    except Exception as error:
        print(f"error performing google translation: {error}")
        return


def detect_language_google(text: str) -> str | None:
    try:
        translator = googletrans.Translator()
        result = translator.detect(text)
        return result.lang.upper()
    except Exception as error:
        print(f"error performing google detect: {error}")
        return
