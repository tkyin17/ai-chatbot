import os
import time
from queue import Queue

SUBTITLE_TXT_PATH = "src/subtitle.txt"


def generate_subtitle(text: str) -> str:
    with open(SUBTITLE_TXT_PATH, "w", encoding="utf-8") as outfile:
        try:
            outfile.write(text.strip('"'))
        except Exception as error:
            print(f"error writing to {SUBTITLE_TXT_PATH}: {error}")


def read_subtitle() -> str:
    with open(SUBTITLE_TXT_PATH, "r", encoding="utf-8") as infile:
        try:
            text = infile.read()
            return text
        except Exception as error:
            print(f"error reading from {SUBTITLE_TXT_PATH}: {error}")


def enqueue_subtitle(queue: Queue) -> None:
    while True:
        if os.path.getsize(SUBTITLE_TXT_PATH):
            queue.put(read_subtitle())
            clear_subtitle()
        # sleep to avoid infinite loops
        time.sleep(0.5)


def clear_subtitle():
    with open(SUBTITLE_TXT_PATH, "w") as f:
        f.truncate(0)
