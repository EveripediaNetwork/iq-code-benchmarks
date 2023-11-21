from pandas import DataFrame
from tqdm import tqdm
from lib.prompts import issues_prediction_prompt
from multiprocessing import Pool
from predictors.main import llm_choices_map


def generate_predictions(df: DataFrame, llm_choices: list[str]):
    """
    Run the predictions on the contracts in the dataset
    this adds {name-of-llm}_prediction columns to the DataFrame
    which contains text of the predicted issues
    """

    # filter llm_choices_map to only include the chosen LLMs
    chosen_llms = []
    for llm in llm_choices_map:
        if llm["name"] in llm_choices:
            chosen_llms.append(llm)

    # Prepare the arguments for multiprocessing
    tasks = []
    for loc, row in df.iterrows():
        for llm in chosen_llms:
            tasks.append((llm, row["code"], loc))

    # Use multiprocessing Pool to run tasks in parallel
    predictions = []
    with Pool(8) as pool:
        p_bar = tqdm(
            pool.imap_unordered(make_prediction, tasks),
            total=len(tasks),
            desc="🧬 Generating predictions",
        )
        for result in p_bar:
            predictions.append(result)

    # Update the DataFrame with the predictions
    for llm_name, prediction, loc in predictions:
        df.loc[loc, f"{llm_name}_prediction"] = prediction


def make_prediction(args) -> tuple[str, str, int]:
    """
    Run the prediction with the given LLM
    """
    llm, contract_code, loc = args
    prompt = issues_prediction_prompt.format(code=contract_code)
    prediction = llm["func"](prompt)
    return llm["name"], prediction, loc
