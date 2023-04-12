import os
import time
from queue import Queue
from pathlib import Path

FILE_NAME = "subtitle.txt"
SUBTITLE_TXT_PATH = Path(__file__).resolve().parent.parent / f"artifacts\{FILE_NAME}"


def generate_subtitle(text: str) -> str:
    with open(SUBTITLE_TXT_PATH, "w", encoding="utf-8") as outfile:
        try:
            outfile.write(text.strip('"'))
        except Exception as error:
            print(f"error writing to {FILE_NAME}: {error}")


def read_subtitle() -> str:
    with open(SUBTITLE_TXT_PATH, "r", encoding="utf-8") as infile:
        try:
            text = infile.read()
            return text
        except Exception as error:
            print(f"error reading from {FILE_NAME}: {error}")


def enqueue_subtitle(queue: Queue) -> None:
    while True:
        if os.path.getsize(SUBTITLE_TXT_PATH):
            queue.put(read_subtitle())
            clear_subtitle()
        else:
            time.sleep(0.5)


def clear_subtitle():
    with open(SUBTITLE_TXT_PATH, "w") as f:
        f.truncate(0)
