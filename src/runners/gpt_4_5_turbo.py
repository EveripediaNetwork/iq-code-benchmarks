from langchain.chat_models import ChatOpenAI


def gpt_3_5_turbo(prompt: str):
    """
    Run the GPT-3.5 Turbo LLM with the given prompt.
    """
    model = ChatOpenAI(model="gpt-4-1106-preview")
    return model.predict(prompt)
