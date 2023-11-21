from predictors.gpt_3_5_turbo import gpt_3_5_turbo
from predictors.gpt_4_turbo import gpt_4_turbo
from pandas import DataFrame
from tqdm import tqdm
from lib.prompts import issues_prediction_prompt

llm_choices_map = [
    {
        "name": "gpt-3.5-turbo",
        "func": gpt_3_5_turbo,
    },
    {
        "name": "gpt-4-turbo",
        "func": gpt_4_turbo,
    },
]


def generate_predictions(df: DataFrame, llm_choices: list[str]):
    """
    Run the prediction with the given LLMs
    """
    # filter llm_choices_map to only include the chosen LLMs
    chosen_llms = list(filter(lambda llm: llm["name"] in llm_choices, llm_choices_map))

    # for every contract in the dataframe, run the prediction with chosen LLMs in parallel
    # then, add the predictions to the dataframe
    # return the dataframe

    predictions_df = df.copy()

    for contract in tqdm(df.iterrows()):
        loc, code = contract[0], contract[1]["code"]

        # run the predictions
        predictions = []
        for llm in chosen_llms:
            prompt = issues_prediction_prompt.format(code=code)
            prediction = llm["func"](prompt)
            predictions.append(prediction)

        # add the predictions to the dataframe
        for i in predictions:
            predictions_df.at[loc, "prediction"] = i

    return predictions_df
