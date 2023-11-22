from pandas import DataFrame
from predictors.gpt_4_turbo import gpt_4_turbo
from lib.prompts import judge_predictions_prompt
from tqdm import tqdm
from json import loads
from termcolor import cprint


def judge_predictions(df: DataFrame, llm_choices: list[str]) -> DataFrame:
    """
    Compare the predictions to the actual issues from the dataset
    and appends {name-of-llm}_correct columns to the DataFrame
    which contains list of issue indices that were correctly predicted
    """
    for llm_name in llm_choices:
        all_false_negatives = []
        all_false_positives = []
        all_true_positives = []

        # loop through each row in the DataFrame and compare the predictions
        # to the actual issues
        p_bar = tqdm(df.iterrows(), total=len(df), desc="🔎 Judging predictions")
        for _, row in p_bar:
            predicted_issues = row[f"{llm_name}_prediction"]
            actual_issues = row["issues"]
            judgement = produce_judgement(actual_issues, predicted_issues)

            all_false_negatives.append(judgement["false_negatives"])
            all_false_positives.append(judgement["false_positives"])
            all_true_positives.append(judgement["true_positives"])

        # update the DataFrame with the judgements
        df[f"{llm_name}_false_negatives"] = all_false_negatives
        df[f"{llm_name}_false_positives"] = all_false_positives
        df[f"{llm_name}_true_positives"] = all_true_positives

    return df


def produce_judgement(actual_issues: str, predicted_issues: str) -> dict:
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

    try:
        # remove the prompt from the result (only keep the json which should start from first { and end with last })
        result = result[result.find("{") : result.rfind("}") + 1]

        # parse the json result
        result = loads(result)

        # return the indices of the issues that were correctly predicted
        return {
            "false_negatives": result["false_negatives"],
            "false_positives": result["false_positives"],
            "true_positives": result["true_positives"],
        }
    except:
        # if the result is not in json format, return an empty dictionary
        cprint(f"🚨 Error parsing judgement: {result}", "white", "on_red")
        return {
            "false_negatives": None,
            "false_positives": None,
            "true_positives": None,
        }


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
