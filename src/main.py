from InquirerPy import prompt
from modules.generate_predictions import generate_predictions
from pandas import DataFrame
from lib.read_toml import read_toml
from dotenv import load_dotenv

load_dotenv()


questions = [
    {
        "type": "checkbox",
        "message": "Pick LLMs to benchmark:",
        "choices": ["gpt-3.5-turbo", "gpt-4-turbo"],
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

    # run the benchmarks
    all_predictions = generate_predictions(df, llm_choices)
    print(all_predictions)

    # TODO: compare predictions to the actual issues from the dataset

    # TODO: save the results to a file
