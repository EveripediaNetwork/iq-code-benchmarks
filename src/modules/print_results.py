from pandas import DataFrame
from termcolor import cprint


def print_results(df: DataFrame, llm_choices: list[str]):
    """
    Print the results of the benchmark to the console
    in a neat table
    """
    results_df = DataFrame()
    for llm_name in llm_choices:
        results_df.loc["Recall", llm_name] = df[f"{llm_name}_recall"].mean()
        results_df.loc["Precision", llm_name] = df[f"{llm_name}_precision"].mean()
        results_df.loc["F1 Score", llm_name] = df[f"{llm_name}_f1_score"].mean()
        results_df.loc["Accuracy", llm_name] = df[f"{llm_name}_accuracy"].mean()
    cprint("🏋️ BENCH RESULTS", "green", attrs=["bold", "underline"])
    print(results_df)
