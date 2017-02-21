from dateutil.tz import tzlocal
import argparse
import datetime as dt
import logging

from rpi_twitter.reader import get_tweets_by_time
from rpi_twitter.t import post_tweet


def get_train_tweets(target_user, trains, start_hour, end_hour, count=100):
    """Return tweets from a target user that mention a certain train.

    Args:
        target_user (str): The user to get tweets from. With out without '@' is
            fine.
        trains (list): A list of trains to look for. Any string is fine, and a
            Tweet will match if it contains that string anywhere.
        start_hour (int): Tweets before this hour of the day will be ignored.
            If None all Tweets are considered.
        end_hour (int): Tweets after this hour of the day will be ignored.
            If None all Tweets are considered.
        count (int): The number of most recent tweets to check.

    Returns:
        list: A list of Status objects from the Tweepy API.
    """
    logging.info("Checking for tweets mention trains: {trains}".format(trains=trains))
    # Set up the time
    now = dt.datetime.now()
    logging.debug("Current datetime: {dt}".format(dt=str(now)))

    if start_hour is not None:
        start_hour = dt.datetime(now.year, now.month, now.day, start_hour, tzinfo=tzlocal())
    logging.debug("Start datetime: {dt}".format(dt=str(start_hour)))
    if end_hour is not None:
        end_hour = dt.datetime(now.year, now.month, now.day, end_hour, tzinfo=tzlocal())
    logging.debug("End datetime: {dt}".format(dt=str(end_hour)))

    # Get all the tweets
    tweets = get_tweets_by_time(target_user, start_hour, end_hour, count)
    logging.info("Found {n} tweets".format(n=str(len(tweets))))

    # Separate out tweets mentioning my trains
    check_tweets = []
    for tweet in tweets:
        text = tweet.text.encode("ascii", "ignore")
        logging.debug("Tweet: {t}".format(t=text))

        # Reject Retweets and replies
        if tweet.retweeted or tweet.in_reply_to_status_id is not None:
            logging.debug("Rejecting Tweet as retweet or reply.")
            continue

        for train in trains:
            if train in text:
                logging.debug("Found a match for train: {train}".format(train=train))
                check_tweets.append(tweet)

    logging.info("Found {n} matching tweets".format(n=str(len(check_tweets))))
    return check_tweets


def main():
    # Command line parsing
    parser = argparse.ArgumentParser(
        prog="Caltrain checker",
        description="Check if @caltrain has mentioned your trains",
    )
    # The list of input files
    parser.add_argument(
        "-t",
        "--trains",
        help="the train number or the string nb/sb to look for, seperated by spaces",
        dest="trains",
        default=None,
        required=True,
        nargs="+",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--user-to-monitor",
        help="the user to monitor for train information",
        dest="target_user",
        default="@caltrain",
    )
    parser.add_argument(
        "-b",
        "--start-time",
        help="the hour to start looking for tweets from",
        dest="start_hour",
        default=None,
        type=int,
    )
    parser.add_argument(
        "-e",
        "--end-time",
        help="the hour to stop looking for tweets at",
        dest="end_hour",
        default=None,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--time-stamp",
        help="add a time stamp to the beginning of the tweet",
        dest="add_time_stamp",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r",
        "--reply-to",
        help="a twitter handle to start the tweet with",
        dest="reply_to",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--n-tweets",
        help="Look at the most recent n tweets, defaults to 100",
        dest="count",
        default=100,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="override the default configuration file",
        dest="conf_file",
        default=None,
    )
    parser.add_argument(
        "--log",
        help="set the logging level, defaults to WARNING",
        dest="log_level",
        default=logging.WARNING,
        choices=[
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL',
        ],
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)

    logging.debug("Arguments: {args}".format(args=args))

    # Check for tweets
    tweets = get_train_tweets(
        args.target_user,
        args.trains,
        args.start_hour,
        args.end_hour,
        args.count,
    )

    # Send Tweet if we found any mentions of our trains
    if tweets:
        contents = "Watch out! @Caltrain mentioned your train in their tweets!"
        post_tweet(
            contents,
            add_time_stamp=args.add_time_stamp,
            reply_to=args.reply_to,
            conf_file=args.conf_file,
        )


if __name__ == "__main__":
    main()
