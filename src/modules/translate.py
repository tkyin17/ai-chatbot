import re
import sys
import deepl
from os import getenv
from dotenv import load_dotenv
from modules.subtitle import generate_subtitle
from modules.katakana import katakana_converter

load_dotenv()

DEEPL_AUTH_TOKEN = getenv("DEEPL_AUTH_TOKEN")

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)
translator = deepl.Translator(DEEPL_AUTH_TOKEN)


def translate_text(text, create_subtitles=False) -> str:
    try:
        # deepl has trouble translating strings with asterisks, convert them to parentheses
        modified_text = re.sub(r"\*([^\*]*)\*", r"(\1)", text)
        # translate EN to JP, need to cast deepl response to str
        translated_text = str(
            translator.translate_text(modified_text, source_lang="EN", target_lang="JA")
        )
        # convert the text to katakana. Example: ORANGE -> オレンジ, so the voice will sound more natural
        katakana_text = katakana_converter(translated_text)
        print("JP Answer: " + katakana_text)
        print("EN Answer: " + text)
        if create_subtitles:
            generate_subtitle(text)
        return katakana_text
    except Exception as error:
        print(f"error translating text: {error}")
        return


# DEEPLX_URL = "http://localhost:1188/translate"


# translate using local deeplx docker container
# def translate_deeplx(
#     text: str, source_language_id: str, target_language_id: str
# ) -> str:
#     # define the parameters for the translation request
#     params = {
#         "text": text,
#         "source_lang": source_language_id,
#         "target_lang": target_language_id,
#     }

#     # convert the parameters to a JSON string
#     payload = json.dumps(params)

#     # send the POST request with the JSON payload
#     response = requests.post(
#         url=DEEPLX_URL, headers={"Content-Type": "application/json"}, data=payload
#     )

#     if response.status_code == 404:
#         print("Unable to reach DeepLx engine, please check that it is running.")
#         return

#     # get the response data as a JSON object
#     data = response.json()

#     # extract the translated text from the response
#     translated_text = data["data"]

#     return translated_text
