import logging
import requests
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tQw


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

roomId = tQw().Global_TAM_UMB_Queue_watcher
# roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vNWMwY2EzZDAtZjI2ZS0xMWVkLTkwYTUtYjdjMTAyNGFjMDZm'

logger = logging.getLogger("Reply message poster")


def reply_to_message(message_id, data):
    """
    Post the replies to initial messages sent from the main TQW program
    :param message_id: Mssage ID from initial message sent to alert TAM of new ticket arrival.
    :param data: Message data including markdown.
    :return: None
    """

    payload = {
        "roomId": roomId,
        "text": data['text'],
        "markdown": data['markdown'],
        'parentId': message_id
    }
    logger.info("Posting messaqe reply to WxT.")
    response = requests.post(f"{tQw().webex_api_url}", headers=tQw().webex_headers, json=payload)
    if response.status_code == 200:
        logger.info("Reply Posted successfully.")


if __name__ == '__main__':
    msgId = 'Y2lzY29zcGFyazovL3VzL01FU1NBR0UvMTQxMTVhMjAtZDY4NS0xMWVlLTg2M2EtZjFiMDZiN2ZkYWU2'
    # roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vNWMwY2EzZDAtZjI2ZS0xMWVkLTkwYTUtYjdjMTAyNGFjMDZm'
    # msg_details = get_msg_details(msgId)
    # roomId = msg_details['roomId']
    # original_message = msg_details['original_message_text']
    # original_sender = msg_details['original_sender']
    # reply_to_message(msgId, roomId, original_message)
