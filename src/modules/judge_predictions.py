from pandas import DataFrame
from predictors.gpt_4_turbo import gpt_4_turbo
from lib.prompts import judge_predictions_prompt


def judge_predictions(df: DataFrame, llm_choices: list[str]) -> None:
    """
    Compare the predictions to the actual issues from the dataset
    and appends {name-of-llm}_correct columns to the DataFrame
    which contains list of issue indices that were correctly predicted
    """
    for llm_name in llm_choices:
        new_correct_col = []

        # loop through each row in the DataFrame and compare the predictions
        # to the actual issues
        for _, row in df.iterrows():
            predicted_issues = row[f"{llm_name}_prediction"]
            actual_issues = row["issues"]
            correct = correct_issues(actual_issues, predicted_issues)
            new_correct_col.append(correct)

        df[f"{llm_name}_correct"] = new_correct_col


def correct_issues(actual_issues: str, predicted_issues: str) -> list[int]:
    """
    Compare the predictions to the actual issues and return the indices of the
    issues that were correctly predicted
    """
    result = gpt_4_turbo(
        judge_predictions_prompt.format(
            key=format_key(actual_issues), prediction=predicted_issues
        )
    )

    correct = []
    if result != "N/A":
        correct = list(map(int, result.split(",")))

    return correct


def format_key(issues: list[str]) -> str:
    """
    Format the issues list to be displayed in the prompt
    """
    return "\n".join([f"{i}: {issues[i]}" for i in range(len(issues))]) + "\n"
