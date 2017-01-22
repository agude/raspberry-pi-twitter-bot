import datetime as dt
import logging
import pytz

from rpi_twitter.helpers import authenticate


def get_tweets_by_time(user, start_time=None, end_time=None, count=100, conf_file=None):
    """Get tweets from a user that appeared between a certain time.

    Tweets matching start_time < tweet.created_at < end_time will be returned.
    *Warning*: We only check their last 100 tweets by default!

    Args:
        user (str): The user to get tweets from. With out without '@' is fine.
        start_time (datetime): Only tweets published after this time are
            returned. If None, then tweets will not be rejected because their
            creation date is too early. Must be an object comparable with an
            offset-aware datetime.
        end_time (datetime): Only tweets published before this time are
            returned. If None, then tweets will not be rejected because their
            creation date is too late. Must be an object comparable with an
            offset-aware datetime.
        count (int): The number of most recent tweets to check.
        conf_file: The location of the Twitter configuration file. If None, the
        standard locations will be searched.

    Returns:
        list: A list of Status objects from the Tweepy API.
    """
    # Get the tweets
    api = authenticate(conf_file=conf_file)
    tweets = api.user_timeline(user, count=count)

    # If the times are None, set the earliest/latest possible dates so that all
    # tweets pass the cut
    if start_time is None:
        logging.debug("Setting start_time to minimum")
        start_time = dt.datetime(dt.MINYEAR, 1, 1, tzinfo=pytz.UTC)

    if end_time is None:
        logging.debug("Setting end_time to maximum")
        end_time = dt.datetime(dt.MAXYEAR, 12, 31, tzinfo=pytz.UTC)

    logging.debug("start_time: {st}".format(st=str(start_time)))
    logging.debug("end_time: {et}".format(et=str(end_time)))
    # Select the correct tweets
    timed_tweets = []
    logging.info("Comparing tweet times")
    for tweet in tweets:
        # Correct the time of the tweet to know that it is UTC
        current_time = tweet.created_at.replace(tzinfo=pytz.UTC)
        tweet.created_at = current_time

        # Too early, so break since tweets are ordered from newest to oldest
        if current_time < start_time:
            logging.debug("Found a tweet with current_time < start_time; breaking")
            break

        # Too late, keep looking
        if current_time > end_time:
            logging.debug("Found a tweet with current_time > end_time; skipping")
            continue

        # Just right!
        timed_tweets.append(tweet)

    return timed_tweets
