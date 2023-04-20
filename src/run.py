from engine.openai import run_openai

# from utils.langchain import run_langchain

MODE = "openai"

if __name__ == "__main__":
    if MODE == "openai":
        run_openai()
    # else:
    #     run_langchain()
