from toml import load, dump
from pandas import DataFrame
import os
from lib.toml_multiline_string_encoder import MultilineStringTomlEncoder


def read_toml(path: str, key=None) -> DataFrame:
    """
    Read a TOML file and return a pandas DataFrame
    """
    with open(path, "r") as f:
        data = load(f)

    if key:
        return DataFrame(data[key])
    return DataFrame(data)


def write_toml(path: str, df: DataFrame, name):
    """
    Write a DataFrame to a TOML file
    """

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    dict = df.to_dict(orient="records")
    dict = {name: dict}

    with open(path, "w") as f:
        dump(dict, f, MultilineStringTomlEncoder())
