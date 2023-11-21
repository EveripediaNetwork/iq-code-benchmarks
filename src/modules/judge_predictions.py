from pandas import DataFrame


def judge_predictions(df: DataFrame, llm_choices: list[str]) -> None:
    """
    Compare the predictions to the actual issues from the dataset
    and appends {name-of-llm}_correct columns to the DataFrame
    which contains list of issue indices that were correctly predicted
    """
    for llm_name in llm_choices:
        correct = []
        for loc, row in df.iterrows():
            predicted_issues = row[f"{llm_name}_prediction"]
            actual_issues = row["issues"]
            if predicted_issues == actual_issues:
                correct.append(loc)
        df[f"{llm_name}_correct"] = correct
