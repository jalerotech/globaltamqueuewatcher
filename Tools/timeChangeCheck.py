import time
import datetime


def is_daylight_saving_time():
    """
    Returns True if the current time is during Daylight Saving Time (DST),
    and False otherwise.
    """
    # Get the current time in local time zone
    local_time = time.localtime()

    # tm_isdst is 1 during DST, 0 if not, and -1 if the information is unavailable
    return bool(local_time.tm_isdst)


if __name__ == "__main__":
    if is_daylight_saving_time():
        print("It is currently Daylight Saving Time.")
    else:
        print("It is not currently Daylight Saving Time.")

