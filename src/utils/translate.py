import sys
import json
import requests
import googletrans

sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)

DEEPLX_URL = "http://localhost:1188/translate"


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


def detect_google(text: str) -> str | None:
    try:
        translator = googletrans.Translator()
        result = translator.detect(text)
        return result.lang.upper()
    except Exception as error:
        print(f"error performing google detect: {error}")
        return
