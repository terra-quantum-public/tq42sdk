import os
import os.path

import tq42.utils.dirs as dirs


def get_current_value(key: str) -> str:
    """
    Get the current value for the provided key in cache file i.e. org, proj..
    If the key was not found raise a KeyError
    """
    if os.path.isfile(dirs.cache_file()):
        with open(dirs.cache_file(), "r") as file:
            for line in file:
                if key in line:
                    split_line = line.strip().split(":")
                    return split_line[1]
    raise KeyError()


def clear_cache() -> None:
    """
    Deletes the content of the cache file.
    """
    # delete context if changing org
    with open(dirs.cache_file(), "w") as file:
        file.truncate()


def write_key_value_to_cache(key: str, value: str) -> None:
    """
    Appends the given tag and id to the cache file
    """
    key_value_line = key + ":" + value

    with open(dirs.cache_file(), "a") as file:
        print(key_value_line, file=file)
