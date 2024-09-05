import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TSE TLs and TSE-Mngrs Availability Message Generator')


def genTSE_TLAnd_Mngrs_on_shift_Msg(tse_on_shift, tse_mngr_on_shift, theatre_data):
    """
    Generated the TSE TLs and TSE Managers on shift alert message using the list of TSE TLs and Managers found to be on not on PTO.
    :param tse_on_shift:
    :param tse_mngr_on_shift:
    :param theatre_data:
    :return: message data in dict format.
    """
    logger.info("Generating TSE TLs and TSE Mngrs on shift message.- STARTED")
    # Managers
    joined_emea_tse = '\n'.join(tse_on_shift["EMEA"])
    joined_us_tse = '\n'.join(tse_on_shift["US"])
    joined_apac_tse = '\n'.join(tse_on_shift["APAC"])

    # Team leads
    joined_emea_tse_TLs = '\n'.join(tse_mngr_on_shift["EMEA"])
    joined_us_tse_TLs = '\n'.join(tse_mngr_on_shift["US"])
    joined_apac_tse_Tls = '\n'.join(tse_mngr_on_shift["APAC"])

    if theatre_data:
        if theatre_data['theatre'] == "EMEA":
            try:
                tos_msg_to_send = f'#### 📌 Available TSE resource(s): \n ' \
                                  f'**EMEA**: \n ' \
                                  f'\n ' \
                                  f'**MANAGER(s)**: \n ' \
                                  f'{joined_emea_tse_TLs} \n ' \
                                  f'\n ' \
                                  f'**TEAM LEAD(s)**: \n ' \
                                  f'{joined_emea_tse} \n '
                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                logger.info(f"Generated TSE TLs and TSE Mngrs on shift Message -> {tos_msg_to_send}")
                logger.info("Generating TSE TLs and TSE Mngrs on shift message.- COMPLETED")
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TSE TLs and TSE Mngrs from that region that's available.")
        if theatre_data['theatre'] == "US":
            try:
                tos_msg_to_send = f'#### 📌 Available TSE resource(s): \n ' \
                                  f'**US**: \n ' \
                                  f'\n ' \
                                  f'**MANAGER(s)**: \n ' \
                                  f'{joined_us_tse_TLs} \n ' \
                                  f'\n ' \
                                  f'**TEAM LEAD(s)**: \n ' \
                                  f'{joined_us_tse} \n '
                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                logger.info(f"Generated TSE TLs and TSE Mngrs on shift Message -> {tos_msg_to_send}")
                logger.info("Generating TAMs on shift message.- COMPLETED")
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TAMs from that region that's available.")
        if theatre_data['theatre'] == "APAC":
            try:
                tos_msg_to_send = f'#### 📌 Available TSE resource(s): \n ' \
                                  f'**APAC**: \n ' \
                                  f'\n ' \
                                  f'**MANAGER(s)**: \n ' \
                                  f'{joined_apac_tse_Tls} \n ' \
                                  f'\n ' \
                                  f'**TEAM LEAD(s)**: \n ' \
                                  f'{joined_apac_tse} \n '

                data = {
                    "text": tos_msg_to_send,
                    "markdown": tos_msg_to_send
                }
                logger.info(f"Generated TSE TLs and TSE Mngrs on shift Message -> {tos_msg_to_send}")
                logger.info("Generating TSE TLs and TSE Mngrs on shift message- COMPLETED")
                return data
            except KeyError as k:
                logger.info(f"Key {k} Missing so no TSE TLs and TSE Mngrs from that region that's available.")

