from predictors.gpt_3_5_turbo import gpt_3_5_turbo
from predictors.gpt_4_turbo import gpt_4_turbo
from pandas import DataFrame
import multiprocess as mp

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

    predictions = df.copy()

    for contract in df.iterrows():
        # use multiprocessing to run the predictions in parallel
        with mp.Pool(processes=len(chosen_llms)) as pool:
            results = pool.map(lambda llm: llm["func"](contract[0]), chosen_llms)

        # add the predictions to the dataframe
        for result in results:
            predictions.loc[contract[0], result["name"]] = result["prediction"]

    return predictions
