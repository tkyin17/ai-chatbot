# import time
# import openai
# import keyboard
# import traceback
# from os import getenv
# from dotenv import load_dotenv
# from modules.prompt import get_identity
# from modules.audio import record_audio, transcribe_audio, generate_audio, play_audio
# from modules.translate import translate_text
# from vits.index import init_vits_model

# load_dotenv()

# MODEL_NAME = getenv("MODEL_NAME")

# messages = []


# def init_openai():
#     openai.api_key = getenv("OPENAI_API_KEY")


# def init_system_prompt():
#     return [{"role": "system", "content": get_identity()}]


# def get_openai_response(input: str):
#     global messages
#     messages.append({"role": "user", "content": input})
#     try:
#         completion = openai.ChatCompletion.create(
#             model=MODEL_NAME, messages=messages, max_tokens=128, temperature=1
#         )
#         response = completion.choices[0].message.content
#         messages.append({"role": "assistant", "content": response})
#         return response
#     except:
#         print("token limit exceeded, clearing messages list and restarting")
#         messages = init_system_prompt()


# def run_openai():
#     try:
#         global messages
#         init_vits_model()
#         init_openai()
#         messages = init_system_prompt()
#         mode = input("Mode (1-Mic): ")
#         if mode == "1":
#             print("Press and Hold Right Shift to record audio")
#             while True:
#                 if keyboard.is_pressed("RIGHT_SHIFT"):
#                     record_audio()
#                     transcribed_text = transcribe_audio()
#                     response_text = get_openai_response(transcribed_text)
#                     translated_text = translate_text(response_text)
#                     generate_audio(translated_text)
#                     play_audio()
#                 else:
#                     # sleep to avoid infinite loops
#                     time.sleep(0.5)
#     except KeyboardInterrupt:
#         print("Stopped")
#     except Exception as error:
#         print(f"an error has occurred: {error}\n{traceback.format_exc()}")
