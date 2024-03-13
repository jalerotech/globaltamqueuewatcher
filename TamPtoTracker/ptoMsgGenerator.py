import logging
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('PTO message generator')


def genPTOMsg(tam_ooo_list, label) -> dict:
    """
    Generated the PTO alert message using the list of TAMS found to be on PTO.
    :param tam_ooo_list:
    :return: message data in dict format.
    """
    logger.info("Generating PTO messages for TAM(s)")
    tam_list_name = []
    joined_tam_list = ''
    for tam in tam_ooo_list:
        if tam['region'] in tqw().EMEA_region:
            tam_list_name.append(f"{tam['name']} (**_EMEA_**)")
            joined_tam_list = '\n'.join(tam_list_name)
        if tam['region'] in tqw().US_region:
            tam_list_name.append(f"{tam['name']} (**_US_**)")
            joined_tam_list = '\n'.join(tam_list_name)
        if tam['region'] in tqw().APAC_region:
            tam_list_name.append(f"{tam['name']} (**_APAC_**)")
            joined_tam_list = '\n'.join(tam_list_name)
    msg_to_send = ''
    if label == "For_CloudSec_Only":
        msg_to_send = f"#### 🛫 CloudSec Team Member(s) on PTO today: \n " \
                      f"{joined_tam_list}"
    if label == "For_TAM_Only":
        msg_to_send = f"#### 🛫 TAM(s) on PTO today: \n " \
                      f"{joined_tam_list}"
    data = {
           "text": msg_to_send,
           "markdown": msg_to_send
       }
    return data


def genTAMS_on_shift_Msg(tams_on_shift, theatre_data):
    """
    Generated the TAMs on shift alert message using the list of TAMS found to be on not on PTO.
    :param tams_on_shift:
    :param theatre_data:
    :return: message data in dict format.
    """
    logger.info("Generating TAMs on shift message.")
    joined_emea_tams = '\n'.join(tams_on_shift["EMEA"])
    joined_us_tams = '\n'.join(tams_on_shift["US"])
    joined_apac_tams = '\n'.join(tams_on_shift["APAC"])
    if theatre_data:
        if theatre_data['theatre'] == "EMEA":
            try:
                tos_msg_to_send = f'#### 📌 TAM(s) on shift: \n ' \
                                  f'**EMEA**: \n ' \
                                  f'{joined_emea_tams} \n '
                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TAMs from that region that's available.")
        if theatre_data['theatre'] == "US":
            try:
                tos_msg_to_send = f'#### 📌 TAM(s) on shift: \n ' \
                                  f'**US**: \n ' \
                                  f'{joined_us_tams} \n '
                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TAMs from that region that's available.")
        if theatre_data['theatre'] == "APAC":
            try:
                tos_msg_to_send = f'#### 📌 TAM(s) on shift: \n ' \
                                  f'**APAC**: \n ' \
                                  f'{joined_apac_tams} \n '
                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TAMs from that region that's available.")
        # try:
    #     tos_msg_to_send = f'#### TAM(s) on shift today \n ' \
    #                       f'**EMEA**: \n ' \
    #                       f'{joined_emea_tams} \n ' \
    #                       f'\n ' \
    #                       f'**US**: \n ' \
    #                       f'{joined_us_tams} \n ' \
    #                       f'\n ' \
    #                       f'**APAC**: \n ' \
    #                       f'{joined_apac_tams} \n '
    #     data = {
    #         "text": tos_msg_to_send,
    #         "markdown": tos_msg_to_send
    #     }
    #     return data
    #
    # except KeyError as k:
    #     logger.info(f"Key {k} Missing so no TAMs from that region that's available.")
    #     return None

