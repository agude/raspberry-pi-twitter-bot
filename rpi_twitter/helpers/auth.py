import logging
import tweepy

try:
    # Works if just run from the directory
    from rpi_twitter.helpers.config import load_config
except ImportError:
    # Works if installed as a package
    from rpi_twitter.helpers import load_config


def authenticate(conf_file=None):
    """Return an authenticated API for Twitter.

    Args:
        conf_file (str): Configuration file to get authentication
            tokens from, if None, use the system default locations for
            the file.
    """
    # Get the authentication tokens
    logging.info("Loading the configuration file")
    logging.debug("Configuration file: '{conf_file}'".format(conf_file=conf_file))
    CONFIG = load_config(conf_file)

    CONSUMER_KEY = CONFIG["consumer_key"]
    CONSUMER_SECRET = CONFIG["consumer_secret"]
    ACCESS_TOKEN = CONFIG["access_token"]
    ACCESS_TOKEN_SECRET = CONFIG["access_token_secret"]

    # Authenticate
    logging.info("Logging into Twitter")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Return an api object
    return api
