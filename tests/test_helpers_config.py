import pytest

import json
import os.path
import random
import string

from rpi_twitter.helpers.config import load_config, read_json


# Some helper functions for the tests
def loaded_dict_test(result):
    assert result.keys() == ["TEST"]
    assert result["TEST"] == ["TEST", "TEST"]


def build_fake_config(path, tmpdir):
    CONT = '{ "TEST": ["TEST", "TEST"] }'

    # Make the new homedirctory
    random_home = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    new_home = tmpdir.mkdir(random_home)

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


def test_RPI_TWITTER_CONFIG(tmpdir, monkeypatch):
    home = build_fake_config("config/rpi-twitter/config", tmpdir)

    # Monkeypatch the environment
    mock_env = {
        "HOME": home,
        "RPI_TWITTER_CONFIG": os.path.join(home, "config", "rpi-twitter", "config"),
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    result = load_config()
    loaded_dict_test(result)


def test_set_XDG_CONFIG_HOME(tmpdir, monkeypatch):
    home = build_fake_config(".config/rpi-twitter/config", tmpdir)
    # Monkeypatch the environment
    mock_env = {
        "HOME": home,
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    result = load_config()
    loaded_dict_test(result)


def test_unset_XDG_CONFIG_HOME(tmpdir, monkeypatch):
    home = build_fake_config(".config/rpi-twitter/config", tmpdir)

    # Monkeypatch the environment
    mock_env = {
        "HOME": home,
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    result = load_config()
    loaded_dict_test(result)


def test_nonstandard_XDG_CONFIG_HOME(tmpdir, monkeypatch):
    home = build_fake_config("config/rpi-twitter/config", tmpdir)

    # Monkeypatch the environment
    mock_env = {
        "HOME": home,
        "XDG_CONFIG_HOME": os.path.join(home, "config"),
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    result = load_config()
    loaded_dict_test(result)


def test_rc_file(tmpdir, monkeypatch):
    home = build_fake_config(".rpitwitterrc", tmpdir)

    # Monkeypatch the environment
    mock_env = {
        "HOME": home,
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    result = load_config()
    loaded_dict_test(result)


def test_load_config_raises(monkeypatch):
    # Monkeypatch the environment
    mock_env = {
        "HOME": "/tmp/",  # Non-sense directory
    }
    monkeypatch.setattr(os, 'environ', mock_env)

    # Test the results
    # With an argument
    with pytest.raises(IOError):
        load_config(None)

    # With default locations
    with pytest.raises(IOError):
        load_config()
