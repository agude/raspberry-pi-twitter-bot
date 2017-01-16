import json
import logging
import os
import os.path


def load_config(config=None):
    """Loads the configuration file for rpi_twitter.

    Args:
        config (str): The location of the configuration json file. If none, it
            looks at the $RPI_TWITTER_CONFIG variable, and then
            ${XDG_CONFIG_HOME}/rpi-twitter/config, and finally
            ${HOME}/.rpitwitterrc.
    """
    logging.info("Loading config file")
    conf_file = None
    if config is not None:
        logging.debug("Config file passed in as a parameter.")
        conf_file = config

    # Try the file at $RPI_TWITTER_CONFIG
    if conf_file is None:
        conf = os.getenv("RPI_TWITTER_CONFIG")
        if conf is not None and os.path.isfile(conf):
            logging.debug("Config file found at $RPI_TWITTER_CONFIG")
            conf_file = conf

    # Try ${XDG_CONFIG_HOME}/rpi-twitter/config
    if conf_file is None:
        backup_conf = os.path.join(os.getenv("HOME"), ".config")
        conf_dir = os.getenv("XDG_CONFIG_HOME", backup_conf)
        conf = os.path.join(conf_dir, "rpi-twitter", "config")
        if os.path.isfile(conf):
            logging.debug("Config file found at ${XDG_CONFIG_HOME}/rpi-twitter/config")
            conf_file = conf

    # Try ${HOME}/.rpitwitterrc
    if conf_file is None:
        conf = os.path.join(os.getenv("HOME"), ".rpitwitterrc")
        if os.path.isfile(conf):
            logging.debug("Config file found at ${HOME}/.rpitwitterrc")
            conf_file = conf

    # If we have failed to find the configuration file, raise an
    # IOError. Otherwise read_json() will fail with a less helpful
    # TypeError.
    if conf_file is None:
        txt = "Configuration file not found!"
        logging.error(txt)
        raise IOError(txt)

    # Return the config dictionary
    logging.info("Returning loaded config")
    return read_json(conf_file)


def read_json(file):
    """Read a JSON file and return the contents.

    Args:
        file (str): Location of the file to open.
    """
    logging.info("Opening JSON file: '{file}'".format(file=file))
    with open(file) as f:
        cont = json.load(f)

    return cont
