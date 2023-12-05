from InquirerPy import prompt
from dotenv import load_dotenv
from modules.generate_predictions import generate_predictions
from modules.judge_predictions import judge_predictions
from modules.calculate_metrics import calculate_metrics
from modules.print_results import print_results
from lib.toml_utils import read_toml
from predictors.main import llm_choices_map
from lib.cache_guard import cache_guard

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
    df = read_toml("data/benchmark.toml", "contracts")

    # run the predictions on the contracts in the dataset
    # this adds {name-of-llm}_prediction columns to the DataFrame
    # which contains text of the predicted issues
    df = cache_guard(generate_predictions, df, llm_choices)

    # compare predictions to the actual issues from the dataset
    # this adds {name-of-llm}_correct columns to the DataFrame
    # which contains list of issue indices that were correctly predicted
    df = cache_guard(judge_predictions, df, llm_choices)

    # calculate metrics based on the predictions and judgement
    # this adds {name-of-llm}_{recall,precision,f1_score,accuracy} columns to the DataFrame
    df = cache_guard(calculate_metrics, df, llm_choices)

    # print the results to the console
    print_results(df, llm_choices)
