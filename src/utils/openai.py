import sys
import time
import openai
import keyboard
from os import getenv
from dotenv import load_dotenv
from utils.prompt import get_identity
from utils.audio import record_and_transcribe_audio
from utils.translate import translate_text

load_dotenv()


OPENAI_API_KEY = getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"

openai.api_key = OPENAI_API_KEY
messages = []


def initMessagesWithSystemPrompt():
    return [{"role": "system", "content": get_identity()}]


def get_openai_response(input: str):
    global messages
    messages.append({"role": "user", "content": input})
    try:
        completion = openai.ChatCompletion.create(model=MODEL_NAME, messages=messages)
        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        return response
    except:
        print("token limit exceeded, clearing messages list and restarting")
        messages = initMessagesWithSystemPrompt()


def run_openai():
    try:
        global messages
        messages = initMessagesWithSystemPrompt()
        mode = input("Mode (1-Mic): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed("RIGHT_SHIFT"):
                    transcribed_text = record_and_transcribe_audio()
                    response_text = get_openai_response(transcribed_text)
                    translate_text(response_text)
                else:
                    # sleep to avoid infinite loops
                    time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as error:
        print(f"an error has occurred: {error}")
