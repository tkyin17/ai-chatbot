# from adapter.openai import run_openai
from adapter.langchain import run_langchain

# openai
# langchain
ADAPTER = "langchain"

if __name__ == "__main__":
    if ADAPTER == "langchain":
        run_langchain()
    # elif ADAPTER == "openai":
    #     run_openai()
    else:
        print("ADAPTER was not specified")
