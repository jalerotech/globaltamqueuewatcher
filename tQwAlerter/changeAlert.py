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
                           f"1. TSEs Team Leads on shift alert. {status[2]} \n "
                           f"2. TSEs Managers on shift alert. {status[2]} \n "}

    changes_data = {"markdown": f"📣 **Changes** : \n " " "
                                f"1. Rewrote Zendesk Data pull/processing logic: \n "
                                f"- Pulling data from Monday.com and storing the data locally (tam-to-customer-mapping.json). \n "
                                f"- Checking the notes on org-level to which the tickets on Zendesk belong. \n "
                                f"- Evaluating the notes and checking if they're viable or not - contains the Primary_TAM, Backup_TAM, Customer_region, BFG_Org_id etc. \n "
                                f"- If the notes are viable, they're used to update the ticket message that's sent to WxT. \n "
                                f"- Otherwise, it uses the locally stored tam-to-customer-mapping for the same purpose. \n "
                    }

    data_list = [fr_data, changes_data]

    for data in data_list:
        webex_response = requests.post(webHookUrl, headers=tQw().webex_headers, json=data)
        if webex_response.status_code == 204:
            logger.info("Successfully posted the changes to the WebHook.")


if __name__ == '__main__':
    changeAlerter()
