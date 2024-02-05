import requests
import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw

logger = logging.getLogger("Change Alerter script.")

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


def changeAlerter() -> None:
    """
    Post latest changes of the scripts and status of feature requests to the WebHook URL on WxH.
    The WebHook point then post the messages to WxT space as soon as it's received.
    :return: None
    """
    # webHookUrl = "https://webexapis.com/v1/webhooks/incoming/Y2lzY29zcGFyazovL3VzL1dFQkhPT0svNmQ0ZDg2NzUtZTkzNS00ZmU5LTg1NTctMzRhMDcyNWU3NTdi"
    webHookUrl = "https://webexapis.com/v1/webhooks/incoming/Y2lzY29zcGFyazovL3VzL1dFQkhPT0svYTkwNzIyYTAtYTgwMC00OTcxLTk0MmMtOTYxYWM1MDc0YmRl"
                                                            # "Y2lzY29zcGFyazovL3VzL1dFQkhPT0svYTkwNzIyYTAtYTgwMC00OTcxLTk0MmMtOTYxYWM1MDc0YmRl"
    status = {
        1: "**Completed** ✅",
        2: "**Ongoing** ⏳",
        3: "**Can't Do** ⛔",
        4: "**Open** 🚏"
    }

    fr_data = {"markdown": f"📝 **Feature/Enhancement Requests** : \n " 
                           f"1. TAMs PTO alert. {status[4]} \n "
                           f"2. TAMs on shift alert. {status[4]} \n "}

    changes_data = {"markdown": f"📣 **Changes** : \n " " "
                                f"1. EMEA time zone updated to CET. \n "
                                f"2. APAC time zone updated. \n "}

    data_list = [fr_data, changes_data]

    for data in data_list:
        webex_response = requests.post(webHookUrl, headers=tQw().webex_headers, json=data)
        if webex_response.status_code == 204:
            logger.info("Successfully posted the changes to the WebHook.")


if __name__ == '__main__':
    changeAlerter()
