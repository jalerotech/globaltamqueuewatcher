import requests
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
import logging
import json


# # Room IDs:
# Global WxT space
roomId = tqw().Global_TAM_UMB_Queue_watcher
# Devs room ID:
# roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vNWMwY2EzZDAtZjI2ZS0xMWVkLTkwYTUtYjdjMTAyNGFjMDZm'


def sendMessageToWxT(data):
    """
    Function for posting messages to WxT, called by other functions when they need to send messages to WxT.

    :param data: Formatted data to be sent to WxT
    :return: None
    """
    logger = logging.getLogger('Message_Poster')
    logger.info("Running sendMessageToWxT function. - STARTED")

    json_data = _add_room_id_to_date(data, None)
    try:
        webex_response = requests.post(tqw().webex_api_url, headers=tqw().webex_headers, json=json_data)
        if webex_response.status_code == 200:
            logger.info(f'Message successfully posted to "Global_TAM_UMB_Queue_watcher" WxT space.')
            logger.info(f"Running sendMessageToWxT function. - COMPLETED")
            return json.loads(webex_response.content)['id']
        else:
            # If the API call was not successful
            logger.info(f"Error in the API call to webex API {webex_response.status_code}: {webex_response.reason}")
            return None
    except Exception as e:
        logger.info(f'Posting to WxT failed with error {e}.')
        return None


def sendMessageToWxT4Cstat(data):
    """
    Function for posting messages to WxT, called by other functions when they need to send messages to WxT.
    :param data: Formatted data to be sent to WxT
    :return: None
    """
    logger = logging.getLogger('Message_Poster')
    logger.info("Running sendMessageToWxT4Cstat function. - STARTED")

    # Cloud Sec TAM Space ID
    cloudSecSpace_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vOGJkNjE4MzAtZGQ1Ni0xMWU4LTlmNWYtOTc3ZWY0YmY5MmQ0'
    json_data = _add_room_id_to_date(data, cloudSecSpace_id)
    # json_data = _add_room_id_to_date(data, roomId)
    try:
        webex_response = requests.post(tqw().webex_api_url, headers=tqw().cstat_webex_headers, json=json_data)
        if webex_response.status_code == 200:
            logger.info(f'Message successfully posted to WxT space.')
            logger.info(f"Running sendMessageToWxT4Cstat function. - COMPLETED")
            return json.loads(webex_response.content)['id']
        else:
            # If the API call was not successful
            logger.info(f"Error in the API call to webex API {webex_response.status_code}: {webex_response.reason}")
            return None
    except Exception as e:
        logger.info(f'Posting to WxT failed with error {e}.')
        return None


def _add_room_id_to_date(data_to_update, cloudSecSpace_id):
    if cloudSecSpace_id:
        data_to_update.update({'roomId': cloudSecSpace_id})
        return data_to_update
    else:
        data_to_update.update({'roomId': roomId})
        return data_to_update


if __name__ == "__main__":
    pass
    # data = {'text': '### New ticket has landed in the TAM Q !!! (1) \n Ticket number: #[1616869](https://opendns.zendesk.com/agent/tickets/1616869) \n Subject: FW: INC3681470 - US-326 - Umbrella Issue reappears \n Company name: **Koninklijke Philips** \n Creation time in UTC: 14:08:10 \nPrimary TAM: Konrad Porzezynski \nBackup TAM(s): Andres Mijael Paredez Marhemberg \nCustomer region:  EMEA \n BFG Link: [ORG_ID:2578504](https://bfg.umbrella.com/organizations/organization/2578504)\n ', 'markdown': '### New ticket has landed in the TAM Q !!! (1) \n Ticket number: #[1616869](https://opendns.zendesk.com/agent/tickets/1616869) \n Subject: FW: INC3681470 - US-326 - Umbrella Issue reappears \n Company name: **Koninklijke Philips** \n Creation time in UTC: 14:08:10 \nPrimary TAM: Konrad Porzezynski \nBackup TAM(s): Andres Mijael Paredez Marhemberg \nCustomer region:  EMEA \n BFG Link: [ORG_ID:2578504](https://bfg.umbrella.com/organizations/organization/2578504)\n '}
    # print(_add_room_id_to_date(data))
