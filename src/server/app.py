import time
import json
import traceback
from os import getenv
from pyngrok import ngrok
from flask_cors import CORS
from flask import Flask, request, Response
from vits.index import init_vits_model, generate_audio
from modules.translate import translate_text
from modules.audio import transcribe_audio
from adapter.langchain import get_langchain_response, init_conversation_chain

# env vars will be exported in colab

NGROK_AUTH_TOKEN = getenv("NGROK_AUTH_TOKEN")
INPUT_WAV_PATH = getenv("INPUT_WAV_PATH")
TTS_WAV_PATH = getenv("TTS_WAV_PATH")
IDENTITY_TXT_PATH = getenv("IDENTITY_TXT_PATH")

# set up flask app
app = Flask(__name__)
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
CORS(app)

# init
conversation_chain = init_conversation_chain()
messages = None


@app.route("/", methods=["GET"])
def test():
    return Response(
        json.dumps({"status": "OK", "message": "Test"}), mimetype="application/json"
    )


@app.route("/messages", methods=["GET"])
def get_messages():
    return Response(json.dumps(messages), mimetype="application/json")


# all in one
@app.route("/generate", methods=["POST"])
def generate():
    global messages

    # get request parameters
    speaker_id = request.args.get("speaker_id")
    audio_data = request.files["audio_file"]

    if speaker_id is None or audio_data is None:
        return Response(
            json.dumps({"message": "missing args", "status": "BAD_REQUEST"}),
            mimetype="application/json",
            status=400,
        )

    # save audio data to lfs
    audio_data.save(INPUT_WAV_PATH)

    # transcribe audio using whisper engine
    transcribed_text = transcribe_audio()

    # send message to gpt engine
    response_text = get_langchain_response(transcribed_text, conversation_chain)

    # translate response
    translated_text = translate_text(response_text)

    # store messages
    messages = {
        "transcribed_text": transcribed_text,
        "translated_text": translated_text,
        "response_text": response_text,
    }

    # synthesize tts
    generate_audio(translated_text, int(speaker_id))

    # read tts.wav as bytes
    with open(TTS_WAV_PATH, "rb") as infile:
        data = infile.read()

    return Response(data, mimetype="audio/wav")


if __name__ == "__main__":
    try:
        # set up vits model
        init_vits_model()

        # open tunnel
        http_tunnel = ngrok.connect(5000)
        print(http_tunnel)

        # start flask app
        app.run()
    except Exception as error:
        print(f"an error has occured: {error}\n{traceback.format_exc()}")
