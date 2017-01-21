import argparse
import logging

from rpi_twitter.helpers import authenticate, timestamp

# Library version
__version__ = "0.1.4"


def post_tweet(contents, add_time_stamp=False, reply_to=None, conf_file=None):
    api = authenticate(conf_file=conf_file)

    # Add a time stamp to the beginning
    time_stamp = ""
    if add_time_stamp:
        time_stamp = timestamp() + ": "
    logging.debug("Time Stamp: '{stamp}'".format(stamp=time_stamp))

    # Add a name to the beginning of the tweet
    reply = ""
    if reply_to is not None:
        if reply_to[0] == "@":
            reply = reply_to.strip() + " "
        else:
            reply = "@" + reply_to.strip() + " "
    logging.debug("Reply to: '{reply}'".format(reply=reply))

    # Assemble the tweet
    tweet = reply + time_stamp + contents
    logging.debug("Tweet: '{tweet}'".format(tweet=tweet))

    if len(tweet) > 140:
        txt = "Tweet is too long: {tweet}".format(tweet=tweet)
        logging.error(txt)
        raise ValueError(txt)

    logging.info("Calling Twitter API to post Tweet.")
    api.update_status(tweet)


def main():
    # Command line parsing
    parser = argparse.ArgumentParser(
        prog="Raspberry Pi Twitter Bot",
        description="Send a tweet",
    )
    # The list of input files
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {ver}'.format(ver=__version__),
    )
    parser.add_argument(
        "tweet",
        type=str,
        help="the content of the tweet"
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
        "-c",
        "--config",
        help="override the default configuration file",
        dest="conf_file",
        default=None,
    )

    args = parser.parse_args()

    logging.debug("Arguments: {args}".format(args=args))

    # Send the tweet
    post_tweet(
        args.tweet,
        add_time_stamp=args.add_time_stamp,
        reply_to=args.reply_to,
        conf_file=args.conf_file,
    )

if __name__ == "__main__":
    main()
