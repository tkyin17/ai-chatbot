import time
import keyboard
import traceback
from os import getenv
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from modules.prompt import get_prompt
from modules.translate import translate_text
from vits.index import init_vits_model, generate_audio
from modules.audio import (
    record_audio,
    transcribe_audio,
    play_audio,
    init_recorder,
)

load_dotenv()

MODEL_NAME = getenv("MODEL_NAME")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")


def init_conversation_chain():
    prompt = get_prompt()
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_key=OPENAI_API_KEY,
        temperature=1,
    )
    memory = ConversationBufferWindowMemory(
        human_prefix="Player",
        ai_prefix="Suisei",
        return_messages=True,
        k=5,
    )
    return ConversationChain(llm=llm, memory=memory, prompt=prompt)


def get_langchain_response(
    query: str,
    converstation_chain: ConversationChain,
):
    return converstation_chain.predict(input=query)


def run_langchain():
    try:
        init_vits_model()
        recorder = init_recorder()
        converstation_chain = init_conversation_chain()
        mode = input("Mode (1-Mic): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed("RIGHT_SHIFT"):
                    record_audio(recorder)
                    transcribed_text = transcribe_audio()
                    response_text = get_langchain_response(
                        transcribed_text, converstation_chain
                    )
                    translated_text = translate_text(response_text)
                    generate_audio(translated_text)
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
