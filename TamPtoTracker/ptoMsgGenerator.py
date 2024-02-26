import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('PTO message generator')


def genPTOMsg(tam_ooo_list) -> dict:
    """
    Generated the PTO alert message using the list of TAMS found to be on PTO.
    :param tam_ooo_list:
    :return: message data in dict format.
    """
    logger.info("Generating PTO messages for TAM(s)")
    tam_list_name = []
    joined_tam_list = ''
    for tam in tam_ooo_list:
        tam_list_name.append(tam['name'])
        joined_tam_list = '\n'.join(tam_list_name)
    msg_to_send = f"### 🛫 TAM(s) on PTO today _(Beta)_: \n " \
                  f"{joined_tam_list}"
    data = {
           "text": msg_to_send,
           "markdown": msg_to_send
       }
    return data
