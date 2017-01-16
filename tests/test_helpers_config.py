import pytest

import json
import os.path

from rpi_twitter.helpers.config import load_config, read_json


# Some helper functions for the tests
def loaded_dict_test(result):
    assert result.keys() == ["TEST"]
    assert result["TEST"] == ["TEST", "TEST"]


def build_fake_config(path, tmpdir):
    CONT = '{ "TEST": ["TEST", "TEST"] }'

    # Make the new homedirctory
    new_home = tmpdir.mkdir("home")

    # Get the file name from the path
    root, file = os.path.split(path)

    # Make a stack of all the directories that need to be made
    dirs = []
    while True:
        root, directory = os.path.split(root)
        if directory:
            dirs.append(directory)
        else:
            if root:
                dirs.append(root)
            break

    # Make the directories
    root = new_home
    for directory in reversed(dirs):  # Reverse because we have a stack
        root = root.mkdir(directory)

    # Make the config file
    root.join(file).write(CONT)

    return new_home.strpath


# The tests
def test_read_json(tmpdir):
    # Write a test file
    CONT = '{ "TEST": ["TEST", "TEST"] }'
    test = tmpdir.join("test.json")
    test.write(CONT)

    # Read it back and check it
    result = read_json(test.strpath)
    loaded_dict_test(result)


def test_load_config_argument(tmpdir):
    home = build_fake_config("config", tmpdir)
    conf_file = os.path.join(home, "config")
    result = load_config(conf_file)


def test_load_config_RPI_TWITTER_CONFIG(tmpdir):
    home = build_fake_config("config/rpi-twitter/config", tmpdir)
    os.environ["RPI_TWITTER_CONFIG"] = os.path.join(home, "config", "rpi-twitter", "config")
    result = load_config()
    loaded_dict_test(result)


def test_load_config_XDG_CONFIG_HOME_set(tmpdir):
    home = build_fake_config(".config/rpi-twitter/config", tmpdir)
    os.environ["XDG_CONFIG_HOME"] = os.path.join(home, ".config")
    result = load_config()
    loaded_dict_test(result)


def test_load_config_XDG_CONFIG_HOME_unset(tmpdir):
    home = build_fake_config(".config/rpi-twitter/config", tmpdir)
    result = load_config()
    loaded_dict_test(result)


def test_load_config_XDG_CONFIG_HOME_nonstandard(tmpdir):
    home = build_fake_config("config/rpi-twitter/config", tmpdir)
    os.environ["XDG_CONFIG_HOME"] = os.path.join(home, "config")
    result = load_config()
    loaded_dict_test(result)


def test_load_config_rc_file(tmpdir):
    home = build_fake_config(".rpitwitterrc", tmpdir)
    result = load_config()
    loaded_dict_test(result)
