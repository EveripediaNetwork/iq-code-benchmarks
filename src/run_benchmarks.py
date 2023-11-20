from runners.gpt_3_5_turbo import gpt_3_5_turbo
from runners.gpt_4_turbo import gpt_4_turbo
from pandas import read_json

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


def run_benchmarks(llm_choices: list[str]):
    """
    Run the benchmark program with the given LLMs
    """

    # Load the benchmark data with pandas
    df = read_json("/data/benchmark.jsonl", lines=True)

    print(df)
