import os

import tq42

CONFIG_FOLDER_NAME = ".tq42sdk"


def full_path(basepath, fn=None):
    basepath = os.path.abspath(basepath)
    if fn is None:
        return basepath
    else:
        return os.path.join(basepath, fn)


def code(fn=None):
    basepath = os.path.dirname(tq42.__file__)
    return full_path(basepath, fn=fn)


def tests(fn=None):
    return full_path(code("tests"), fn=fn)


def testdata(fn=None):
    return full_path(tests("testdata"), fn=fn)


def text_files_dir(fn=None):
    return full_path(code("utils/text_files"), fn=fn)


def test_data_dir(fn=None):
    return full_path(code("tests/testdata"), fn=fn)


def cache_dir(fn=None):
    return text_files_dir(fn=fn)


def cache_file():
    return cache_dir("__tq42__.dat")


def config(fn=None):
    return full_path(create_or_get_config_dir(), fn=fn)


def create_or_get_config_dir(alt_config_folder=None):
    package_dir = (
        alt_config_folder if alt_config_folder is not None else get_config_folder_path()
    )

    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

    return package_dir


def get_config_folder_path():
    home_dir = os.path.expanduser("~")
    package_dir = os.path.join(home_dir, CONFIG_FOLDER_NAME)
    return package_dir
