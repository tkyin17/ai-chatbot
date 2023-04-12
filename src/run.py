import sys
import time
import wave
import json
import openai
import pyaudio
import winsound
import keyboard
from common.config import *
from utils.voicevox import *
from utils.subtitle import *
from utils.translate import *
from utils.prompt_maker import *

# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)

openai.api_key = OPENAI_API_KEY

conversation = []
# Create a dictionary to hold the message data
history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
transcribed_message = ""
chat_prev = ""
is_Speaking = False
owner_name = "yin"


# function to get the user's input audio
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    frames = []
    print("Recording...")
    while keyboard.is_pressed("RIGHT_SHIFT"):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()
    transcribe_audio("input.wav")


# function to transcribe the user's audio
def transcribe_audio(file):
    global transcribed_message
    try:
        audio_file = open(file, "rb")

        # Translating the audio to English
        # transcript = openai.Audio.translate("whisper-1", audio_file)

        # Transcribe the audio to detected language
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        transcribed_message = transcript.text
        print("Question: " + transcribed_message)
    except Exception as error:
        print(f"error transcribing audio: {error}")
        return

    result = owner_name + " said " + transcribed_message
    conversation.append({"role": "user", "content": transcribed_message})
    openai_answer()


# function to get an answer from OpenAI
def openai_answer():
    global total_characters, conversation

    total_characters = sum(len(d["content"]) for d in conversation)

    while total_characters > 4000:
        try:
            # print(total_characters)
            # print(len(conversation))
            conversation.pop(2)
            total_characters = sum(len(d["content"]) for d in conversation)
        except Exception as error:
            print(f"error removing old messages: {error}")

    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = get_prompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt, max_tokens=128, temperature=1, top_p=0.9
    )
    message = response["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": message})

    translate_text(message)


# translating is optional
def translate_text(text):
    global is_Speaking
    # subtitle will act as subtitle for the viewer
    # subtitle = translate_google(text, "ID")

    # tts will be the string to be converted to audio
    detect = detect_google(text)
    # tts = translate_google(text, f"{detect}", "JA")
    tts = translate_deeplx(text, f"{detect}", "JA")
    tts_en = translate_google(text, f"{detect}", "EN")
    try:
        # print("ID Answer: " + subtitle)
        print("JP Answer: " + tts)
        print("EN Answer: " + tts_en)
    except Exception as error:
        print(f"error printing text: {error}")
        return

    # Choose between the available TTS engines
    # Japanese TTS
    get_voicevox_tts(tts)

    # Generate subtitle
    generate_subtitle(text)

    time.sleep(1)

    # is_Speaking is used to prevent the assistant speaking more than one audio at a time
    is_Speaking = True
    winsound.PlaySound("output.wav", winsound.SND_FILENAME)
    is_Speaking = False


def preparation():
    global conversation, transcribed_message, chat, chat_prev
    while True:
        # If the assistant is not speaking, and the chat is not empty, and the chat is not the same as the previous chat
        # then the assistant will answer the chat
        transcribed_message = chat
        if is_Speaking == False and transcribed_message != chat_prev:
            # Saving chat history
            conversation.append({"role": "user", "content": transcribed_message})
            chat_prev = transcribed_message
            openai_answer()
        time.sleep(1)


if __name__ == "__main__":
    try:
        mode = input("Mode (1-Mic): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed("RIGHT_SHIFT"):
                    record_audio()
                else:
                    # sleep to avoid infinite loops
                    time.sleep(0.5)

    except KeyboardInterrupt:
        print("Stopped")
