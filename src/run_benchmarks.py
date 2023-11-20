from runners.gpt_3_5_turbo import gpt_3_5_turbo
from runners.gpt_4_turbo import gpt_4_turbo
from pandas import DataFrame
from lib.read_toml import read_toml

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

    df = DataFrame(read_toml("data/benchmark.toml")["contracts"])

    print(df)
