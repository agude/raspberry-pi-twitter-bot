# Raspberry Pi Twitter Bot

[![Build Status](https://travis-ci.org/agude/raspberry-pi-twitter-bot.svg?branch=master)](https://travis-ci.org/agude/raspberry-pi-twitter-bot)

Raspberry Pi Twitter Bot (RPTB) is a commandland utility to send Tweets to
Twitter using Python and [Tweepy](https://github.com/tweepy/tweepy).

## Installation

Since RPTB is still pre-1.0, the only way to install it is to clone this
repository and run `pip install .` in the directory with `setup.py`. This will
install the library, and the command line tool `t` which is used to send
tweets.

## Configuration

RPTB requires a configuration file with Twitter keys in it. The file should
contain the following:

```json
{
  "consumer_key": "SomeKey",
  "consumer_secret": "AnotherKey",
  "access_token": "AccessToken",
  "access_token_secret": "AnotherToken",
}
```

This will will be searched for at the following locations (and it will stop at
the first one it finds):

- `$RPI_TWITTER_CONFIG`
- `$XDG_CONFIG_HOME/rpi-twitter/config`
- `$HOME/.rpitwitterrc`

Note that you can define whatever you'd like for for `$RPI_TWITTER_CONFIG` as
long as it points to a valid JSON file with the correct object, otherwise note
that there is no `.json` extension on `config` or `.rpitwitterrc`.

## Usage

Once your configuration is in place, you can send Tweets as follows:

`t 'This is a Tweet! #MyFirstRobotTweet'`

Which results in a tweet like: This is a Tweet! #MyFirstRobotTweet

A time stamp can be added to the beginning:

`t -s 'This tweet has a timestamp!'`

Which results in a tweet like: 12:34:56: This tweet has a timestamp!

Finally, a status can be sent to a single other user as follows:

`t 'Help help! I\'m being oppressed!' -r '@alex_gude'`

Which results in a tweet like: @alex_gude Help help! I'm being oppressed

A custom config to override the default file can be specified with `-c`:

`t -c ~/myconfig 'Tweet tweet'`

If you try to send a tweet that is too long, the program raises an
`ValueError` and does not post the Tweet.
