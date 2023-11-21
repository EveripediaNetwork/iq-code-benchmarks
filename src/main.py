from InquirerPy import prompt
from pandas import DataFrame
from dotenv import load_dotenv
from modules.generate_predictions import generate_predictions
from modules.judge_predictions import judge_predictions
from lib.read_toml import read_toml
from predictors.main import llm_choices_map

load_dotenv()


questions = [
    {
        "type": "checkbox",
        "message": "Pick LLMs to benchmark:",
        "choices": map(lambda llm: llm["name"], llm_choices_map),
        "validate": lambda result: len(result) >= 1,
        "invalid_message": "should be at least 1 selection",
        "instruction": "(select at least 1)",
    },
]


if __name__ == "__main__":
    """
    Script to run the benchmark program
    """
    result = prompt(questions)
    llm_choices = result[0]

    # get the benchmark dataset
    df = DataFrame(read_toml("data/benchmark.toml")["contracts"])

    # run the predictions on the contracts in the dataset
    # this adds {name-of-llm}_prediction columns to the DataFrame
    # which contains text of the predicted issues
    generate_predictions(df, llm_choices)

    # compare predictions to the actual issues from the dataset
    # this adds {name-of-llm}_correct columns to the DataFrame
    # which contains list of issue indices that were correctly predicted
    judge_predictions(df, llm_choices)

    # TODO: save the results to a file
