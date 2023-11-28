from pandas import DataFrame


def calculate_metrics(df: DataFrame, llm_choices: list[str]) -> DataFrame:
    """
    Calculate metrics for each LLM

    We collect the following metrics:
    - Recall [True Positive / (True Positive + False Negative)]
    - Precision [True Positive / (True Positive + False Positive)]
    - F1 Score [2 * (Precision * Recall) / (Precision + Recall)]
    - Accuracy  [True Positive + True Negative / (True Positive + False Positive + False Negative + True Negative)]
    """

    metrics_df = DataFrame()
    metrics_df.columns = ["model", "recall", "precision", "f1_score", "accuracy"]

    for llm_name in llm_choices:
        true_positives = df[f"{llm_name}_true_positives"].sum()
        false_positives = df[f"{llm_name}_false_positives"].sum()
        false_negatives = df[f"{llm_name}_false_negatives"].sum()

        recall = true_positives / (true_positives + false_negatives)
        precision = true_positives / (true_positives + false_positives)
        f1_score = 2 * (precision * recall) / (precision + recall)

        metrics_df = metrics_df.append(
            {
                "model": llm_name,
                "recall": recall,
                "precision": precision,
                "f1_score": f1_score,
                "accuracy": (true_positives + true_positives)
                / (true_positives + false_positives + false_negatives + true_positives),
            },
            ignore_index=True,
        )

    return metrics_df
