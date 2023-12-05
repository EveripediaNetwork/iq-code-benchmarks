from predictors.gpt_3_5_turbo import gpt_3_5_turbo
from predictors.gpt_4_turbo import gpt_4_turbo
from predictors.sol_auditor_v1 import sol_auditor_v1

"""
Contains the list of LLMs that can be used for benchmarking
Make sure to list the predictor functions here when adding a new LLM
to test. 

Predictor functions should take a string as input and return a string
"""
llm_choices_map = [
    {
        "name": "gpt-3.5-turbo",
        "func": gpt_3_5_turbo,
    },
    {
        "name": "gpt-4-turbo",
        "func": gpt_4_turbo,
    },
    {"name": "sol-auditor-v1", "func": sol_auditor_v1},
]
