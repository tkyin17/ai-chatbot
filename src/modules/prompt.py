from langchain.prompts import PromptTemplate

IDENTITY_FILE_PATH = "src/character/identity.txt"


def get_identity():
    with open(IDENTITY_FILE_PATH, "r", encoding="utf-8") as infile:
        try:
            identity = infile.read()
            return identity
        except Exception as error:
            print(f"error reading identity.txt: {error}")


def get_prompt():
    template = f"""{get_identity()}
Summary of conversation:
{{history}}
Current conversation:
User: {{input}}
Assistant:"""
    prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    print(prompt.format_prompt(history="", input="hello").to_messages())
    return prompt
