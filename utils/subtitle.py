import time
import os


def generate_subtitle(text):
    # output.txt will be used to display the subtitle on OBS
    with open("output.txt", "w", encoding="utf-8") as outfile:
        try:
            outfile.write(text.strip('"'))

        except:
            print("Error writing to output.txt")


def read_subtitle():
    with open("output.txt", "r", encoding="utf-8") as infile:
        try:
            text = infile.read()
            return text
        except:
            print("Error reading from output.txt")


def enqueue_subtitle(queue):
    while True:
        if os.path.getsize("output.txt"):
            text = read_subtitle()
            print(f"placing subtitles into queue: {text}")
            queue.put(text)
            clear_output()
        else:
            time.sleep(0.5)


def clear_output():
    time.sleep(1)
    with open("output.txt", "w") as f:
        f.truncate(0)
