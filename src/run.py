import sys
import time
import keyboard
from utils.voicevox import *
from utils.subtitle import *
from utils.translate import *
from utils.prompt import *
from utils.audio import *
from utils.langchain import get_gpt_response

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)


if __name__ == "__main__":
    try:
        mode = input("Mode (1-Mic): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed("RIGHT_SHIFT"):
                    transcribed_text = record_audio()
                    response_text = get_gpt_response(transcribed_text)

                else:
                    # sleep to avoid infinite loops
                    time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as error:
        print(f"an error has occurred: {error}")
