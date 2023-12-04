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
        avg_toy_f1_score = (
            results_df.loc["F1 Score"].filter(lambda x: x["type"] == "toy").mean()
        )
        avg_real_f1_score = (
            results_df.loc["F1 Score"].filter(lambda x: x["type"] == "real").mean()
        )
        results_df.loc["IQ Score", llm_name] = (
            0.2 * avg_toy_f1_score + 0.8 * avg_real_f1_score
        )
    cprint("🏋️ BENCH RESULTS", "green", attrs=["bold", "underline"])
    print(results_df)
