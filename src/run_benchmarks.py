from runners.gpt_3_5_turbo import gpt_3_5_turbo
from runners.gpt_4_5_turbo import gpt_4_turbo

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


def run_benchmark(llm_choices: list[str]):
    """
    Run the benchmark program with the given LLMs
    in parallel.
    """
