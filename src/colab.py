import sys
import time
import keyboard
import traceback
import requests
import argparse
from os import getenv
from dotenv import load_dotenv
from modules.audio import record_audio, play_audio, init_recorder

load_dotenv()

SPEAKER_ID = getenv("SPEAKER_ID")
INPUT_WAV_PATH = getenv("INPUT_WAV_PATH")
TTS_WAV_PATH = getenv("TTS_WAV_PATH")


def generate_tts(base_url):
    try:
        # send input audio
        with open(INPUT_WAV_PATH, "rb") as infile:
            files = {"audio_file": infile.read()}
            r = requests.post(
                f"{base_url}/generate?speaker_id={SPEAKER_ID}",
                files=files,
            )

        # write tts wav to file
        with open(TTS_WAV_PATH, "wb") as outfile:
            outfile.write(r.content)

        # get messages
        r = requests.get(f"{base_url}/messages")
        messages = r.json()

        print(f"You: {messages['transcribed_text']}")
        print(f"JP Answer: {messages['translated_text']}")
        print(f"EN Answer: {messages['response_text']}")
    except requests.exceptions.Timeout:
        print("request timeout")
    return


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--url", type=str)
        args = parser.parse_args()
        base_url = args.url
        if base_url is None:
            print("no base url specified")
            sys.exit()

        recorder = init_recorder()
        mode = input("Mode (1-Mic): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed("RIGHT_SHIFT"):
                    record_audio(recorder)
                    generate_tts(base_url)
                    play_audio()
                else:
                    # sleep to avoid infinite loops
                    time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped")
        # call terminate() to clear PortAudio resources
        recorder.terminate()
    except Exception as error:
        print(f"an error has occurred: {error}\n{traceback.format_exc()}")
