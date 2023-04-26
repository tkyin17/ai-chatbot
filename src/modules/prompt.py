from os import getenv
from dotenv import load_dotenv
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    AIMessagePromptTemplate,
)

load_dotenv()

IDENTITY_TXT_PATH = getenv("IDENTITY_TXT_PATH")


def get_identity():
    with open(IDENTITY_TXT_PATH, "r", encoding="utf-8") as infile:
        try:
            return infile.read()
        except Exception as error:
            print(f"error reading identity.txt: {error}")


def get_prompt():
    template = f"""{get_identity()}
Summary of current conversation:"""
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(template),
            MessagesPlaceholder(variable_name="history"),
            # for some reason, human_prefix and ai_prefix needs to be defined here as extra args
            # to prevent the response from switching to third person
            HumanMessagePromptTemplate.from_template("{input}", human_prefix="Player"),
            AIMessagePromptTemplate.from_template("", ai_prefix="Suisei"),
        ]
    )
    return prompt
