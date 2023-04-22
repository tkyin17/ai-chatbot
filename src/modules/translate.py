import sys
import json
import requests
from modules.subtitle import generate_subtitle

DEEPLX_URL = "http://localhost:1188/translate"
TTS_WAV_PATH = "src/artifacts/tts.wav"

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)


def translate_text(text) -> str:
    # translate EN to JP
    translated_text = translate_deeplx(text, "EN", "JA")
    try:
        print("JP Answer: " + translated_text)
        print("EN Answer: " + text)
    except Exception as error:
        print(f"error translating text: {error}")
        return
    generate_subtitle(text)
    return translated_text


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

    if response.status_code == 404:
        print("Unable to reach DeepLx engine, please check that it is running.")
        return

    # get the response data as a JSON object
    data = response.json()

    # extract the translated text from the response
    translated_text = data["data"]

    return translated_text
