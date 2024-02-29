import logging
from TamPtoTracker.getPersonDataWebEx import get_users_status
from TamPtoTracker.ptoMsgGenerator import genPTOMsg
from ticketAndMsgHandlers.msgPoster import sendMessageToWxT
from tqwMainClass.tamQueueWatcherClass import TamQueueWatcher as tqw
from TamPtoTracker.TamPTOMsgDataGenerator import tamPTOMsgDataWriter

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('TAM PTO Bot')

tam_in_ooo_export = []


def ptoWatcherMain(label) -> list:
    logger.info(f"Running the PTO Watcher Main function with a fixed list of TAM resources.")
    """
    Runs the main PTO programs using the imported modules "get_users_status", "genPTOMsg" and "sendMessageToWxT".
    :param:
    :return: None
    """

    tam_in_ooo = get_users_status(tqw().list_of_tam)
    if label == 'local':
        return tam_in_ooo
    else:
        pto_msg = genPTOMsg(tam_in_ooo)
        sendMessageToWxT(pto_msg)
        tamPTOMsgDataWriter(tam_in_ooo)


#
# def _return_tam_ooo_list():
#     return tam_in_ooo_export
#
#
# def returnTAMStatus(tam_name) -> str:
#     for tam in tam_in_ooo:
#         if tam['name'] == tam_name:
#             tamPtoLabelName = f"{tam_name} 🛫"
#             return tamPtoLabelName


if __name__ == '__main__':
    ptoWatcherMain("Not_local")
    # user_email = ['anattwoo@cisco.com', 'aely@cisco.com', 'jalero@cisco.com',
    #               'aparedez@cisco.com', 'arjraina@cisco.com', 'ajavaher@cisco.com', 'bewallac@cisco.com',
    #               'brparnel@cisco.com', 'ccoral@cisco.com', 'ccardina@cisco.com', 'dforcade@cisco.com',
    #               'diebarra@cisco.com', 'hputra@cisco.com', 'harmeije@cisco.com', 'ianave@cisco.com',
    #               'halijenn@cisco.com', 'jesshepp@cisco.com', 'jonleduc@cisco.com', 'kahowes@cisco.com',
    #               'kajus@cisco.com', 'kevhudso@cisco.com', 'kporzezr@cisco.com', 'kvindas@cisco.com',
    #               'magainer@cisco.com', 'mneibert@cisco.com', 'nnwobodo@cisco.com', 'paulth2@cisco.com',
    #               'pwijenay@cisco.com',
    #               'sknez@cisco.com', 'tarrashi@cisco.com', 'tingwa2@cisco.com', 'ugandhi@cisco.com',
    #               'wgardeaz@cisco.com',
    #               'xiaoshya@cisco.com', 'yusito@cisco.com']
    # ptoWatcherMain(user_email)
