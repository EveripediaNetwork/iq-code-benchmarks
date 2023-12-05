from pandas import DataFrame


def calculate_metrics(df: DataFrame, llm_choices: list[str]) -> DataFrame:
    """
    Calculate metrics for each LLM

    We collect the following metrics:
    - Recall [True Positive / (True Positive + False Negative)]
    - Precision [True Positive / (True Positive + False Positive)]
    - F1 Score [2 * (Precision * Recall) / (Precision + Recall)]
    - F2 Score [(1 + 2^2) * (Precision * Recall) / (2^2 * Precision + Recall)]
    - Accuracy  [True Positive / (True Positive + False Positive + False Negative)]
    """

    for llm_name in llm_choices:
        for i, row in df.iterrows():
            true_positive = len(row[f"{llm_name}_true_positives"])
            false_positive = len(row[f"{llm_name}_false_positives"])
            false_negative = len(row[f"{llm_name}_false_negatives"])

            recall = true_positive / (true_positive + false_negative)
            precision = true_positive / (true_positive + false_positive)

            if precision + recall == 0:
                f1_score = 0
                f2_score = 0
            else:
                f1_score = 2 * (precision * recall) / (precision + recall)
                f2_score = (
                    (1 + 2**2) * (precision * recall) / (2**2 * precision + recall)
                )
            accuracy = true_positive / (true_positive + false_positive + false_negative)

            df.loc[i, f"{llm_name}_recall"] = recall
            df.loc[i, f"{llm_name}_precision"] = precision
            df.loc[i, f"{llm_name}_f1_score"] = f1_score
            df.loc[i, f"{llm_name}_f2_score"] = f2_score
            df.loc[i, f"{llm_name}_accuracy"] = accuracy

    return df
