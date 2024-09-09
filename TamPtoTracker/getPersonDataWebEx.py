import requests
import logging
import json
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')


def ret_team_ooo(tam_email_list) -> list:
    logger.info("Returning List of Team members that are Out Of Office. - STARTED")
    """
    Returns a list of Team members with status set to OutOfOffice - Not only TAM.
    """
    ooo_tams = []
    country_list = []
    for tam_email in tam_email_list:
        # Passing the email as a parameter -> this is needed for the @ symbol on the email be encoded with the "urllib.parse" lib.
        params = {
            "email": tam_email
        }
        url = f'{tqw().webex_base_url}people'
        webex_resp = requests.get(url, params=params, headers=tqw().webex_headers)
        for country in json.loads(webex_resp.content)['items'][0]['addresses']:
            country_list.append(country['country'])
        status = json.loads(webex_resp.content)['items'][0]['status']
        displayName = json.loads(webex_resp.content)['items'][0]['displayName']
        email = json.loads(webex_resp.content)['items'][0]['emails']
        region = json.loads(webex_resp.content)['items'][0]['addresses'][0]['country']
        if displayName == "Chris Stewart":
            if status == 'OutOfOffice':
                if email in tqw().tse_TLs:
                    msg_data = {
                        'name': f"{displayName}{'TEAM LEAD'}",
                        'status': status,
                        'email': email,
                        'region': 'CN'
                    }
                    ooo_tams.append(msg_data)
        if status == 'OutOfOffice':
            if email in tqw().tse_TLs:
                msg_data = {
                    'name': f"{displayName}{'TEAM LEAD'}",
                    'status': status,
                    'email': email,
                    'region': region
                }
                ooo_tams.append(msg_data)
            else:
                msg_data = {
                    'name': displayName,
                    'status': status,
                    'email': email,
                    'region': region
                }
                ooo_tams.append(msg_data)
    logger.info("Returning List of Team members that are Out Of Office. - COMPLETED")
    logger.info(f"Returning list -> {ooo_tams}")
    return ooo_tams


def ret_available_tams(email_list) -> dict:
    logger.info("Returning Dict of TAMs that are available. - STARTED")
    """
    Returns a list of available TAMs with no OOO set.
    Produces a dict with a list of all available TAMs per region.
    """
    tams_on_shift = {
        "EMEA": [],
        "APAC": [],
        "US": []
    }
    country_list = []
    for email in email_list:
        # Passing the email as a parameter -> this is needed for the @ symbol on the email be encoded with the "urllib.parse" lib.
        params = {
            "email": email
        }
        url = f'{tqw().webex_base_url}people'
        webex_resp = requests.get(url, params=params, headers=tqw().webex_headers)
        for country in json.loads(webex_resp.content)['items'][0]['addresses']:
            country_list.append(country['country'])
        status = json.loads(webex_resp.content)['items'][0]['status']
        displayName = json.loads(webex_resp.content)['items'][0]['displayName']
        if displayName == "Chris Stewart":
            region = 'AU'
        else:
            region = json.loads(webex_resp.content)['items'][0]['addresses'][0]['country']
        if status != 'OutOfOffice':
            if email in tqw().tse_TLs:
                if region in tqw().EMEA_region:
                    tams_on_shift["EMEA"].append(f"{displayName} {'(_TL_)'}")
                if region in tqw().US_region:
                    tams_on_shift["US"].append(f"{displayName} {'(_TL_)'}")
                if region in tqw().APAC_region:
                    tams_on_shift["APAC"].append(f"{displayName} {'(_TL_)'}")
            else:
                if region in tqw().EMEA_region:
                    tams_on_shift["EMEA"].append(displayName)
                if region in tqw().US_region:
                    tams_on_shift["US"].append(displayName)
                if region in tqw().APAC_region:
                    tams_on_shift["APAC"].append(displayName)
    logger.info("Returning Dict of TAMs that are available. - COMPLETED")
    logger.info(f"Returned Dict -> {tams_on_shift}.")
    return tams_on_shift


if __name__ == '__main__':
    user_email = ['anattwoo@cisco.com', 'aely@cisco.com', 'ianave@cisco.com']
    print(ret_available_tams(tqw().tams))
