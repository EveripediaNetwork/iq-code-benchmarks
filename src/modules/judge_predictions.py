from pandas import DataFrame
from predictors.gpt_4_turbo import gpt_4_turbo
from lib.prompts import judge_predictions_prompt
from tqdm import tqdm


def judge_predictions(df: DataFrame, llm_choices: list[str]) -> DataFrame:
    """
    Compare the predictions to the actual issues from the dataset
    and appends {name-of-llm}_correct columns to the DataFrame
    which contains list of issue indices that were correctly predicted
    """
    for llm_name in llm_choices:
        new_correct_col = []

        # loop through each row in the DataFrame and compare the predictions
        # to the actual issues
        p_bar = tqdm(df.iterrows(), total=len(df), desc="🔎 Judging predictions")
        for _, row in p_bar:
            predicted_issues = row[f"{llm_name}_prediction"]
            actual_issues = row["issues"]
            correct = correct_issues(actual_issues, predicted_issues)
            new_correct_col.append(correct)

        df[f"{llm_name}_correct"] = new_correct_col

    return df


def correct_issues(actual_issues: str, predicted_issues: str) -> list[int]:
    """
    Compare the predictions to the actual issues and return the indices of the
    issues that were correctly predicted. This uses gpt-4-turbo to compare the
    issues.
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
    key = []
    for i, issue in enumerate(issues):
        category = issue["category"]
        description = issue["description"]
        location = issue["location"]
        impact = issue["impact"]

        key.append(
            f"{i + 1}) category: {category}\ndescription: {description}\nlocation: {location}\nimpact: {impact}\n"
        )
    return "\n".join(key)
