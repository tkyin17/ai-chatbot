from os import getenv
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI
from utils.prompt import get_prompt

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-3.5-turbo"

prompt = get_prompt()
llm = ChatOpenAI(model_name=MODEL_NAME, openai_api_key=OPENAI_API_KEY)
memory = ConversationSummaryMemory(llm=llm)
conversation = ConversationChain(llm=llm, memory=memory, prompt=prompt, verbose=True)


def get_gpt_response(query: str):
    response = conversation.predict(input=query)
    print(f"Response: {response}")
    return response
