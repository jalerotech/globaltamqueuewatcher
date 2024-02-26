import requests
import logging
import json
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')


def get_users_status(tam_email_list):
    """

    :param tam_email_list:
    :return:
    """
    logger.info("Getting user...")
    ooo_tams = []
    country_list = []
    for tam_email in tam_email_list:
        url = f'{tqw().webex_base_url}people?email={tam_email}'
        webex_resp = requests.get(url, headers=tqw().webex_headers)
        for country in json.loads(webex_resp.content)['items'][0]['addresses']:
            country_list.append(country['country'])
        status = json.loads(webex_resp.content)['items'][0]['status']
        displayName = json.loads(webex_resp.content)['items'][0]['displayName']
        email = json.loads(webex_resp.content)['items'][0]['emails']
        region = json.loads(webex_resp.content)['items'][0]['addresses'][0]['country']
        if status == 'OutOfOffice':
            msg_data = {
                'name': displayName,
                'status': status,
                'email': email,
                'region': region
            }
            ooo_tams.append(msg_data)
    return ooo_tams


if __name__ == '__main__':
    user_email = ['anattwoo@cisco.com', 'aely@cisco.com', 'ianave@cisco.com']
    get_users_status(user_email)

