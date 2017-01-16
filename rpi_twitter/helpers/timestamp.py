import datetime
import logging
import time


def timestamp():
    """ Return the current timestamp as a string: "HH:MM:SS". """
    logging.info("Getting time")
    current_time = datetime.datetime.now()
    return time.strftime("%H:%M:%S", current_time.timetuple())
