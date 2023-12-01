import os
from lib.toml_utils import read_toml, write_toml
from termcolor import cprint


def cache_guard(func, df, *args, **kwargs):
    """
    This function is used to wrap other functions that take a DataFrame as an argument
    It will check if a cached DataFrame exists at the given path
    If it does, it will pass the cached DataFrame to the wrapped function

    This also caches the result of the wrapped function to the given path
    """
    cache_path = f"cache/{func.__name__}_output.toml"

    # If the cache file exists, load it and pass it to the wrapped function
    if os.path.exists(cache_path):
        cprint(f"🚧 Using cached DataFrame from {cache_path}", "blue", "on_yellow")
        # overwrite the df argument with the cached DataFrame
        return read_toml(cache_path, "contracts")

    # If the cache file does not exist, run the wrapped function
    # and save the result to the cache file
    df = func(df, *args, **kwargs)
    write_toml(cache_path, df, "contracts")

    return df
