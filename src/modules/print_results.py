from pandas import DataFrame
from termcolor import cprint


def print_results(df: DataFrame, llm_choices: list[str]):
    """
    Print the results of the benchmark to the console
    in a neat table

    This aggregates the results of the benchmark
    with the following metrics:
    - Average Recall
    - Average Precision
    - Average F1 Score
    - Average Accuracy
    - IQ Score (weighted average of F1 Score on toy and real datasets)
    """
    results_df = DataFrame()
    for llm_name in llm_choices:
        results_df.loc["Recall", llm_name] = df[f"{llm_name}_recall"].mean()
        results_df.loc["Precision", llm_name] = df[f"{llm_name}_precision"].mean()
        results_df.loc["F1 Score", llm_name] = df[f"{llm_name}_f1_score"].mean()
        results_df.loc["F2 Score", llm_name] = df[f"{llm_name}_f2_score"].mean()
        results_df.loc["Accuracy", llm_name] = df[f"{llm_name}_accuracy"].mean()

        avg_toy_f1_score = df[df["type"] == "toy"][f"{llm_name}_f1_score"].mean()
        avg_real_f1_score = df[df["type"] == "real"][f"{llm_name}_f1_score"].mean()

        results_df.loc["IQ Score", llm_name] = (
            0.2 * avg_toy_f1_score + 0.8 * avg_real_f1_score
        )
    cprint("🏋️ BENCH RESULTS", "green", attrs=["bold", "underline"])
    print(results_df)
