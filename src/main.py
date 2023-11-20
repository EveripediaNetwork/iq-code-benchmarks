"""
    Script to run the benchmark program
"""
from InquirerPy import prompt
from modules.run_benchmarks import run_benchmarks

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
    result = prompt(questions)
    llm_choices = result[0]
    run_benchmarks(llm_choices)
