from predictors.gpt_3_5_turbo import gpt_3_5_turbo
from predictors.gpt_4_turbo import gpt_4_turbo
from pandas import DataFrame

llm_choices = [
    {
        "name": "gpt-3.5-turbo",
        "func": gpt_3_5_turbo,
    },
    {
        "name": "gpt-4-turbo",
        "func": gpt_4_turbo,
    },
]


def generate_predictions(df: DataFrame, llm_choices: list[str]):
    """
    TODO: Run the prediction with the given LLMs
    """
